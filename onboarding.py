import discord
import os

# ============================================================
# CONFIGURATION
# ============================================================
ROLE_FR = "Membre Legacyz"
ROLE_EN = "Legacyz International"
CHANNEL_LOUNGE_FR = 1361686684911141087
CHANNEL_LOUNGE_EN = 1397117269024440351  # world-lounge

# ============================================================
# TEXTE ONBOARDING FR
# ============================================================

DM_FR_1 = """
╔══════════════════════════════════════╗
         **BIENVENUE DANS LE CLUB** ⚽️
╚══════════════════════════════════════╝

Tu viens de rejoindre l'une des communautés les plus passionnées autour des **cartes de collection sportives** et de l'univers **Club Legacyz**.

Ici, on partage, on collectionne, on échange, on se challenge et on évolue **ensemble**.

Prends quelques minutes pour découvrir ton nouvel espace — cette expérience a été conçue pour toi. 👇
"""

DM_FR_2 = """
**🎭 LES RÔLES DE LA COMMUNAUTÉ**

Voici les différents rôles que tu croiseras :

👑 **@Founders** → L'équipe officielle Club Legacyz
🎨 **@Legacyz Designer** → Référent design & direction artistique
🏗️ **@Builder** → Responsable du Discord & de la communauté
🛡️ **@Modo Legacyz** → Respect des règles + animation & gestion
🤝 **Helpers** *(soon)* → Membres dédiés à t'accueillir et répondre à tes questions
⭐ **@Ultra Legacyz** → Membres historiques avec accès à des espaces exclusifs
🃏 **@Membre Legacyz** → C'est toi ! Tous les membres classiques de la communauté
🌍 **@Legacyz International** → Membres internationaux

> Si tu as une question → contacte un **Helper**
> Si tu as un problème → contacte **@Modo Legacyz** : @Keut 💊comicbook ou @Jules
"""

DM_FR_3 = """
**📍 STRUCTURE DU DISCORD**

**📢 News**
`#annonces` → Toutes les infos officielles, drops et updates importantes

**🏠 Welcome**
`#politique-de-moderation` → Les règles officielles + la culture du Club
`#fiche-membre` → Ta présentation personnelle *(un guide est dispo)*
`#ticket` → Questions, réclamations, demandes privées

**👥 Legacyz Member — Ton espace**
`#lounge` → Discussions générales, ambiance conviviale
`#event-legacyz` → Infos sur les événements physiques
`#legacyz-pass` → Programme de fidélité & compétition communautaire
`#five-legacyz` → Construis ton équipe de 5 cartes
`#collection-room` → Partage tes cartes & ouvertures
`#exclusivité-backstage` → Contenu exclusif non publié sur les réseaux
`#idées-membres` → Propose tes idées pour faire évoluer le Club
`#faq` → Questions & réponses publiques
`#live-opening` → Ouvre ton pack en direct

**🔁 Trading**
`#trading-time` → Cartes disponibles à l'échange *(utilise le tag 🇫🇷 [FR])*
`#wanted-cards` → Cartes que tu recherches
`#avis-échanges` → Retours et réputation après échanges
`#ebay-tracker` → Annonces eBay en direct — ta référence marché
"""

DM_FR_4 = """
**🏆 LES ATHLÈTES ICONS FOOTBALL CARDS**

Des légendes et stars du football mondial ont signé pour toi. Voici les athlètes de la collection **Icons** :

🇧🇷 Raphinha · 🇭🇷 Luka Modric · 🇧🇷 Ronaldinho · 🇪🇸 Fermin Lopez
🇧🇷 Roberto Carlos · 🇺🇾 Federico Valverde · 🇪🇸 Andrés Iniesta
🇫🇷 Bradley Barcola · 🇪🇸 Xavi · 🇫🇷 Eduardo Camavinga
🇨🇮 Yaya Touré · 🇪🇸 Fabian Ruiz · 🇨🇿 Pavel Nedved
🇬🇳 Serhou Guirassy · 🇫🇷 Lucas Hernandez · 🇮🇹 Filippo Inzaghi
🇫🇷 Djibril Cissé · 🇵🇹 Deco · 🇫🇷 Ibrahima Konaté
🏴󠁧󠁢󠁥󠁮󠁧󠁿 Michael Owen · 🇫🇷 Corentin Tolisso · 🇧🇪 Eden Hazard
🇫🇷 Raphaël Varane · 🇦🇷 Javier Pastore · 🇪🇸 Javi Guerra
🇫🇷 Maxence Caqueret · 🇵🇹 Pauleta · 🇫🇷 Robert Pirès
🇪🇸 Antonio Cordero · 🇫🇷 Ludovic Giuly · 🇳🇬 Jay-Jay Okocha
🇫🇷 Loïc Rémy · 🇪🇸 Jesus Rodriguez · 🇫🇷 Fabien Barthez

> Chaque carte est signée **on card**, de la main de l'athlète. Une pièce unique qui raconte son héritage. 🖊️
"""

DM_FR_5 = """
**🚀 TES 3 PREMIÈRES ACTIONS**

Pour plonger immédiatement dans l'expérience Club Legacyz :

**1️⃣ Présente-toi**
→ Rends-toi dans `#fiche-membre` et présente-toi à la communauté. Un guide est disponible dans le salon pour t'aider.

**2️⃣ Rejoins le Legacyz Pass**
→ Direction `#legacyz-pass` — c'est le programme de fidélité & de compétition de la communauté. Accumule des XP, monte dans le classement et débloque des récompenses exclusives.

**3️⃣ Partage ta collection**
→ Poste tes cartes dans `#collection-room` ou lance-toi dans le trading via `#trading-time`. La communauté est là pour trader, échanger et challenger.

══════════════════════════════════════
Bienvenue encore une fois. Tu fais désormais partie de l'aventure.
**Ici, on ne fait pas qu'observer : on construit l'histoire Club Legacyz ensemble.** 🏆

*Prêt à entrer dans le Club ?* ⚽️
"""

# ============================================================
# TEXTE ONBOARDING EN
# ============================================================

DM_EN_1 = """
╔══════════════════════════════════════╗
       **WELCOME TO THE CLUB** ⚽️
╚══════════════════════════════════════╝

You just joined one of the most passionate communities around **sports trading cards** and the **Club Legacyz** universe.

Here, we share, collect, trade, challenge each other and grow **together**.

Take a few minutes to discover your new space — this experience has been designed for you. 👇
"""

DM_EN_2 = """
**🎭 COMMUNITY ROLES**

Here are the different roles you'll encounter:

👑 **@Founders** → The official Club Legacyz team
🎨 **@Legacyz Designer** → Design lead & artistic direction
🏗️ **@Builder** → Discord & community manager
🛡️ **@Modo Legacyz** → Rules enforcement + moderation & animation
🤝 **Helpers** *(soon)* → Members dedicated to welcoming and guiding you
⭐ **@Ultra Legacyz** → Long-standing members with access to exclusive spaces and decisions
🃏 **@Membre Legacyz** → All standard community members
🌍 **@Legacyz International** → That's you — international members with their own dedicated space

> Have a question? → Reach out to a **Helper**
> Have a dispute or issue? → Contact **@Modo Legacyz** directly
"""

DM_EN_3 = """
**📍 DISCORD STRUCTURE & CHANNEL GUIDE**

**📢 News**
`#announcements` → All official info, drops, updates and important news *(EN)*

**🌍 Welcome & Profile**
`#politique-de-moderation` → Official rules & community values
`#member-profile` → Your personal introduction *(a guide is available)*
`#ticket` → Questions, complaints, disputes, private requests

**🌐 World — Your Space**
`#world-lounge` → General discussions, chill vibes, get to know the community
`#world-collection` → Share your cards, openings & personal showcases
`#next-level` → Dedicated to the upcoming international programme — stay tuned 👀
`#feedback` → Share your thoughts to help us improve the experience

**👀 FR Space — Observer Mode**
`#collection-room` → Browse FR members' collections and get inspired
`#live-opening` → Watch pack openings live with the community

**🔁 Trading — Global Space**
`#trading-time` → Cards available for trade *(use 🇬🇧 [EN] tag on your posts)*
`#wanted-cards` → Cards you're looking for *(use 🇬🇧 [EN] tag)*
`#ebay-tracker` → Live eBay listings & completed sales — your market reference
"""

DM_EN_4 = """
**🏆 ICONS FOOTBALL CARDS — THE ATHLETES**

Legends and stars of world football have signed for you. Here are the athletes of the **Icons** collection:

🇧🇷 Raphinha · 🇭🇷 Luka Modric · 🇧🇷 Ronaldinho · 🇪🇸 Fermin Lopez
🇧🇷 Roberto Carlos · 🇺🇾 Federico Valverde · 🇪🇸 Andrés Iniesta
🇫🇷 Bradley Barcola · 🇪🇸 Xavi · 🇫🇷 Eduardo Camavinga
🇨🇮 Yaya Touré · 🇪🇸 Fabian Ruiz · 🇨🇿 Pavel Nedved
🇬🇳 Serhou Guirassy · 🇫🇷 Lucas Hernandez · 🇮🇹 Filippo Inzaghi
🇫🇷 Djibril Cissé · 🇵🇹 Deco · 🇫🇷 Ibrahima Konaté
🏴󠁧󠁢󠁥󠁮󠁧󠁿 Michael Owen · 🇫🇷 Corentin Tolisso · 🇧🇪 Eden Hazard
🇫🇷 Raphaël Varane · 🇦🇷 Javier Pastore · 🇪🇸 Javi Guerra
🇫🇷 Maxence Caqueret · 🇵🇹 Pauleta · 🇫🇷 Robert Pirès
🇪🇸 Antonio Cordero · 🇫🇷 Ludovic Giuly · 🇳🇬 Jay-Jay Okocha
🇫🇷 Loïc Rémy · 🇪🇸 Jesus Rodriguez · 🇫🇷 Fabien Barthez

> Every card is signed **on card**, directly by the athlete's hand. A unique piece that tells their legacy. 🖊️
"""

DM_EN_5 = """
**🚀 YOUR FIRST 3 ACTIONS**

Dive straight into the Club Legacyz experience:

**1️⃣ Introduce yourself**
→ Head to `#member-profile` and introduce yourself to the community. A guide is available in the channel.

**2️⃣ Join the NEXT LEVEL programme**
→ Check out `#next-level` — something big is coming for international members. Be among the first in. 👀

**3️⃣ Start trading**
→ Post your cards in `#trading-time` using the 🇬🇧 [EN] tag, or browse `#wanted-cards` to find what you're looking for. The community is here to trade, exchange and challenge.

══════════════════════════════════════
Welcome to the Club. You're not just here to watch.
**You're here to be part of the Club Legacyz story.** 🏆

*Ready to enter the Club?* ⚽️
"""

# ============================================================
# MESSAGES PUBLICS DE BIENVENUE
# ============================================================

def welcome_message_fr(member):
    return f"""
🎉 **Bienvenue à {member.mention} !**

Un nouveau membre vient de rejoindre l'aventure Club Legacyz. Accueillez-le comme il se doit ! 🃏⚽️

> N'hésite pas à te présenter dans `#fiche-membre` et à rejoindre le `#legacyz-pass` pour commencer à accumuler des XP dès aujourd'hui.

*Bienvenue dans le Club, la communauté est là pour toi.* 🏆
"""

def welcome_message_en(member):
    return f"""
🎉 **Welcome {member.mention}!**

A new international member just joined the Club Legacyz adventure. Give them a warm welcome! 🃏⚽️

> Don't forget to introduce yourself in `#member-profile` and keep an eye on `#next-level` — something big is coming. 👀

*Welcome to the Club — the community is here for you.* 🏆
"""

# ============================================================
# FONCTION PRINCIPALE D'ONBOARDING
# ============================================================

async def send_onboarding(member, role_name, client):
    """Envoie la séquence d'onboarding complète selon le rôle"""

    is_fr = role_name == ROLE_FR
    is_en = role_name == ROLE_EN

    if not is_fr and not is_en:
        return

    # Séquence DM
    try:
        dm_messages = [DM_FR_1, DM_FR_2, DM_FR_3, DM_FR_4, DM_FR_5] if is_fr else [DM_EN_1, DM_EN_2, DM_EN_3, DM_EN_4, DM_EN_5]
        for msg in dm_messages:
            await member.send(msg)

    except discord.Forbidden:
        print(f"Impossible d'envoyer un DM à {member.name} (DMs désactivés)")

    # Message public dans le bon lounge
    channel_id = CHANNEL_LOUNGE_FR if is_fr else CHANNEL_LOUNGE_EN
    channel = client.get_channel(channel_id)
    if channel:
        welcome_msg = welcome_message_fr(member) if is_fr else welcome_message_en(member)
        await channel.send(welcome_msg)
    else:
        print(f"Canal introuvable : {channel_id}")
