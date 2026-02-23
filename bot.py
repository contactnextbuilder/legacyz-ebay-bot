import discord
import aiohttp
import asyncio
import base64
import os
from datetime import datetime
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


async def search_ebay(token):
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
                print(f"Erreur eBay API: {resp.status} - {await resp.text()}")
                return None


def build_embed(item, item_type):
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
    elif item_type == "FIXED":
        color = COLOR_BUY_NOW
        emoji = "🔵"
        type_label = "ACHAT IMMÉDIAT"
        description = f"**Prix :** {price}"
    else:
        color = COLOR_SOLD
        emoji = "🟢"
        type_label = "VENDU"
        description = f"**Prix de vente :** {price}"

    embed = discord.Embed(
        title=f"{emoji} {title}",
        url=url,
        description=description,
        color=color,
        timestamp=datetime.now(datetime.UTC)
    )
    embed.set_author(name=f"eBay • {type_label}")
    embed.add_field(name="Vendeur", value=seller, inline=True)
    embed.add_field(name="État", value=condition, inline=True)
    embed.add_field(name="🔗 Voir l'annonce", value=f"[Cliquer ici]({url})", inline=False)
    if image_url:
        embed.set_thumbnail(url=image_url)
    embed.set_footer(text="Legacyz eBay Tracker")
    return embed


async def check_ebay():
    await client.wait_until_ready()
    channel = client.get_channel(DISCORD_CHANNEL_ID)
    if not channel:
        print(f"Canal Discord introuvable : {DISCORD_CHANNEL_ID}")
        return
    print("Bot démarré — surveillance eBay active...")
    while not client.is_closed():
        try:
            token = await get_ebay_token()
            if not token:
                await asyncio.sleep(CHECK_INTERVAL)
                continue
            results = await search_ebay(token)
            if results and "itemSummaries" in results:
                for item in results["itemSummaries"]:
                    item_id = item.get("itemId")
                    if item_id in seen_items:
                        continue
                    seen_items.add(item_id)
                    buying_options = item.get("buyingOptions", [])
                    item_type = "AUCTION" if "AUCTION" in buying_options else "FIXED"
                    embed = build_embed(item, item_type)
                    await channel.send(embed=embed)
                    await asyncio.sleep(1)
        except Exception as e:
            print(f"Erreur eBay: {e}")
        await asyncio.sleep(CHECK_INTERVAL)


@client.event
async def on_ready():
    print(f"✅ Bot connecté : {client.user}")
    client.loop.create_task(check_ebay())


@client.event
async def on_member_update(before, after):
    """Déclenche l'onboarding quand un membre reçoit un rôle FR ou EN"""
    before_roles = {r.name for r in before.roles}
    after_roles = {r.name for r in after.roles}
    new_roles = after_roles - before_roles

    for role_name in new_roles:
        if role_name in [ROLE_FR, ROLE_EN]:
            print(f"Nouveau rôle détecté : {role_name} pour {after.name}")
            await send_onboarding(after, role_name, client)
            break


client.run(DISCORD_TOKEN)
