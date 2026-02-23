import discord
import aiohttp
import asyncio
import base64
import os
from datetime import datetime, timezone
from onboarding import send_onboarding, ROLE_FR, ROLE_EN

# ============================================================
# CONFIGURATION — Variables d'environnement Railway
# ============================================================
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
EBAY_APP_ID = os.environ.get("EBAY_APP_ID")
EBAY_CERT_ID = os.environ.get("EBAY_CERT_ID")
DISCORD_CHANNEL_ID = 1474452023075405834
SEARCH_KEYWORD = "Club Legacyz"
CHECK_INTERVAL = 300
# ============================================================

COLOR_SOLD = 0x00C853
COLOR_AUCTION = 0xFFD600
COLOR_BUY_NOW = 0x2196F3

seen_items = set()
seen_sold_items = set()

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)


async def get_ebay_token():
    credentials = base64.b64encode(f"{EBAY_APP_ID}:{EBAY_CERT_ID}".encode()).decode()
    headers = {
        "Authorization": f"Basic {credentials}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = "grant_type=client_credentials&scope=https://api.ebay.com/oauth/api_scope"
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://api.ebay.com/identity/v1/oauth2/token",
            headers=headers,
            data=data
        ) as resp:
            result = await resp.json()
            return result.get("access_token")


async def search_ebay_active(token):
    """Annonces actives via Browse API"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-EBAY-C-MARKETPLACE-ID": "EBAY_FR"
    }
    params = {"q": SEARCH_KEYWORD, "limit": 20}
    url = "https://api.ebay.com/buy/browse/v1/item_summary/search"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                print(f"Erreur eBay Browse API: {resp.status}")
                return None


async def search_ebay_sold():
    """Ventes terminées via Finding API"""
    url = "https://svcs.ebay.com/services/search/FindingService/v1"
    params = {
        "OPERATION-NAME": "findCompletedItems",
        "SERVICE-VERSION": "1.0.0",
        "SECURITY-APPNAME": EBAY_APP_ID,
        "RESPONSE-DATA-FORMAT": "JSON",
        "keywords": SEARCH_KEYWORD,
        "itemFilter(0).name": "SoldItemsOnly",
        "itemFilter(0).value": "true",
        "paginationInput.entriesPerPage": "10",
        "sortOrder": "EndTimeSoonest"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                print(f"Erreur eBay Finding API: {resp.status}")
                return None


def build_embed_active(item, item_type):
    title = item.get("title", "Annonce sans titre")
    url = item.get("itemWebUrl", "")
    price_info = item.get("price", {})
    price = f"{price_info.get('value', '?')} {price_info.get('currency', 'EUR')}"
    image_url = item.get("thumbnailImages", [{}])[0].get("imageUrl", None) if item.get("thumbnailImages") else None
    condition = item.get("condition", "Non précisé")
    seller = item.get("seller", {}).get("username", "Vendeur inconnu")

    if item_type == "AUCTION":
        color = COLOR_AUCTION
        emoji = "🟡"
        type_label = "ENCHÈRE EN COURS"
        bid_count = item.get("bidCount", 0)
        end_date = item.get("itemEndDate", "")
        description = f"**Prix actuel :** {price}\n**Offres :** {bid_count}\n**Fin :** {end_date[:16].replace('T', ' ') if end_date else 'N/A'}"
    else:
        color = COLOR_BUY_NOW
        emoji = "🔵"
        type_label = "ACHAT IMMÉDIAT"
        description = f"**Prix :** {price}"

    embed = discord.Embed(
        title=f"{emoji} {title}",
        url=url,
        description=description,
        color=color,
        timestamp=datetime.now(timezone.utc)
    )
    embed.set_author(name=f"eBay • {type_label}")
    embed.add_field(name="Vendeur", value=seller, inline=True)
    embed.add_field(name="État", value=condition, inline=True)
    embed.add_field(name="🔗 Voir l'annonce", value=f"[Cliquer ici]({url})", inline=False)
    if image_url:
        embed.set_thumbnail(url=image_url)
    embed.set_footer(text="Legacyz eBay Tracker")
    return embed


def build_embed_sold(item):
    """Construit l'embed pour une vente terminée"""
    title = item.get("title", ["Annonce sans titre"])[0]
    url = item.get("viewItemURL", [""])[0]
    price = item.get("sellingStatus", [{}])[0].get("currentPrice", [{}])[0].get("__value__", "?")
    currency = item.get("sellingStatus", [{}])[0].get("currentPrice", [{}])[0].get("@currencyId", "EUR")
    bid_count = item.get("sellingStatus", [{}])[0].get("bidCount", ["0"])[0]
    end_time = item.get("listingInfo", [{}])[0].get("endTime", [""])[0]
    seller = item.get("sellerInfo", [{}])[0].get("sellerUserName", ["Inconnu"])[0]
    image_url = item.get("galleryURL", [None])[0]

    end_display = end_time[:16].replace("T", " ") if end_time else "N/A"

    embed = discord.Embed(
        title=f"🟢 {title}",
        url=url,
        description=f"**Prix de vente final :** {price} {currency}\n**Nombre d'offres :** {bid_count}\n**Vendu le :** {end_display}",
        color=COLOR_SOLD,
        timestamp=datetime.now(timezone.utc)
    )
    embed.set_author(name="eBay • VENDU ✅")
    embed.add_field(name="Vendeur", value=seller, inline=True)
    embed.add_field(name="🔗 Voir l'annonce", value=f"[Cliquer ici]({url})", inline=False)
    if image_url:
        embed.set_thumbnail(url=image_url)
    embed.set_footer(text="Legacyz eBay Tracker — Référence marché")
    return embed


async def check_ebay():
    await client.wait_until_ready()
    channel = client.get_channel(DISCORD_CHANNEL_ID)
    if not channel:
        print(f"Canal Discord introuvable : {DISCORD_CHANNEL_ID}")
        return

    print("Bot démarré — surveillance eBay active (annonces + ventes terminées)...")

    while not client.is_closed():
        try:
            token = await get_ebay_token()

            # --- Annonces actives ---
            if token:
                results = await search_ebay_active(token)
                if results and "itemSummaries" in results:
                    for item in results["itemSummaries"]:
                        item_id = item.get("itemId")
                        if item_id in seen_items:
                            continue
                        seen_items.add(item_id)
                        buying_options = item.get("buyingOptions", [])
                        item_type = "AUCTION" if "AUCTION" in buying_options else "FIXED"
                        embed = build_embed_active(item, item_type)
                        await channel.send(embed=embed)
                        await asyncio.sleep(1)

            # --- Ventes terminées ---
            sold_results = await search_ebay_sold()
            if sold_results:
                try:
                    items = sold_results["findCompletedItemsResponse"][0]["searchResult"][0].get("item", [])
                    for item in items:
                        item_id = item.get("itemId", [""])[0]
                        if item_id in seen_sold_items:
                            continue
                        seen_sold_items.add(item_id)
                        embed = build_embed_sold(item)
                        await channel.send(embed=embed)
                        await asyncio.sleep(1)
                except (KeyError, IndexError) as e:
                    print(f"Erreur parsing ventes terminées: {e}")

        except Exception as e:
            print(f"Erreur générale eBay: {e}")

        await asyncio.sleep(CHECK_INTERVAL)


@client.event
async def on_ready():
    print(f"✅ Bot connecté : {client.user}")
    client.loop.create_task(check_ebay())


@client.event
async def on_member_update(before, after):
    before_roles = {r.name for r in before.roles}
    after_roles = {r.name for r in after.roles}
    new_roles = after_roles - before_roles
    for role_name in new_roles:
        if role_name in [ROLE_FR, ROLE_EN]:
            print(f"Nouveau rôle détecté : {role_name} pour {after.name}")
            await send_onboarding(after, role_name, client)
            break


client.run(DISCORD_TOKEN)
