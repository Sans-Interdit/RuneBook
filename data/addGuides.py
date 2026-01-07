from data.models import Tag, Guide, session as db_session

def addGuide(title, content, tags, difficulty):
    # Check if guide already exists
    existing_guide = db_session.query(Guide).filter_by(title=title).first()
    if existing_guide:
        print(f"Guide already exists: {title}")
        return

    # Create and attach guide immediately
    new_guide = Guide(
        title=title,
        content=content,
        level=difficulty,
        id_source=2,
    )
    db_session.add(new_guide)

    # Add tags
    for tag_name in tags:
        with db_session.no_autoflush:
            tag = db_session.query(Tag).filter_by(name=tag_name).first()

        if not tag:
            tag = Tag(name=tag_name)
            db_session.add(tag)

        new_guide.tags.append(tag)

    db_session.commit()

    print(f"Guide added: {new_guide.title} with difficulty {new_guide.level}")





title = "Rôles des joueurs - Répartition et responsabilités"

content = """Dans une partie classique de League of Legends, chaque équipe est composée de cinq joueurs, chacun occupant un rôle précis, associé à une position de départ sur la carte. Cette répartition permet une distribution équilibrée de l'or et de l'expérience au sein de l'équipe.

Un joueur commence sur la voie du haut (toplane), un autre sur la voie du milieu (midlane), tandis que deux joueurs débutent sur la voie du bas (botlane). Sur cette dernière, on retrouve généralement un carry AD (ADC), chargé d'infliger des dégâts sur la durée, accompagné d’un support, dont le rôle est de protéger, assister et contrôler les ennemis. Ces quatre joueurs évoluent principalement sur leur voie en début de partie et cherchent à accumuler de l'or et de l'expérience en éliminant les sbires adverses, tout en empêchant leurs opposants directs d'en faire autant.

Le cinquième joueur est le jungler. Il commence la partie dans la jungle, où il élimine des monstres neutres afin de gagner de l'or et de l'expérience. En plus de cette progression personnelle, le jungler a un rôle clé de soutien global : il se déplace entre les voies pour surprendre les ennemis (ganks), aider ses alliés en difficulté et sécuriser des objectifs importants.

Au fil de la partie, les rôles deviennent plus flexibles. Les joueurs quittent progressivement leurs voies initiales pour se regrouper, combattre en équipe et prendre des objectifs majeurs. Bien que chaque rôle ait des responsabilités spécifiques, la coopération et l’adaptation sont essentielles pour mener l’équipe à la victoire.

Grâce à l'expérience accumulée, les champions montent de niveau, améliorant leurs statistiques et leurs compétences. L'or gagné permet quant à lui d'acheter des objets, renforçant encore davantage leur puissance. Une bonne compréhension de son rôle et de ses priorités est fondamentale pour progresser et contribuer efficacement au succès de l'équipe."""
 
tags = ["Rôles", "Lanes", "Gameplay", "Fondamentaux"]

difficulty = "New Player"

addGuide(title, content, tags, difficulty)




title = "Farming - Vue d'ensemble"

content = """Le farming consiste à éliminer des vagues de sbires et des camps de monstres, afin de gagner de l'expérience et de l'or. Au sein d'une équipe, les champions chargés d'obtenir la majorité de ces ressources par le farming peuvent ou non jouer le rôle de carry ; cependant, tous les carrys sont censés farmer.

Le farming est essentiel en phase de laning, lorsque les laners (le toplaner, le midlaner et le bottom carry) tentent de dominer l'ennemi en apprenant de nouvelles compétences et en accumulant des ressources. Le jungler, quant à lui, a accès aux monstres de la jungle pour rivaliser avec les laners. Les rotations de lanes impliquent souvent une distribution optimale des ressources issues des éliminations de sbires à un moment précis de la partie.

Le jeu comptabilise les creeps tués sous forme de score, le Creep Score (CS) : tuer un seul sbire rapporte 1 point, tuer un camp entier de monstres rapporte 4 points. Le CS par minute (CSPM) est une mesure qui peut être utilisée pour évaluer les performances relatives des rôles de farm et de carry au sein d'un jeu ou à travers les rangs."""

tags = ["Gameplay", "Farming", "Présentation", "Bases"]

difficulty = "New Player"


addGuide(title, content, tags, difficulty)




title = "Farming - Fondamentaux"

content = """Afin d'optimiser la répartition de l'or et la puissance défensive en fonction des ressources disponibles sur la carte, un champion est chargé de farmer les sbires sur chaque voie (le laner) et un autre de farmer la jungle (le jungler). Les déplacements entre les voies sont minimes en cours de partie et quasi inexistants en début de partie. L'objectif général pour tous les rôles de farm est d'équilibrer le temps et les efforts consacrés au farm avec les autres aspects du jeu.

Les laners doivent éliminer les sbires dès leur apparition afin de défendre leurs structures, tout en accumulant de l'or et de l'expérience pour gagner en puissance. Tuer un monstre garantit au tueur l'intégralité de sa récompense en or et en expérience. Les sbires ennemis qui meurent partagent passivement leur récompense d'expérience entre tous les alliés proches. En portant le coup fatal à un sbire, le tueur est assuré de recevoir sa récompense en or, ainsi que sa part d'expérience, quelle que soit la distance. Ce coup, appelé « last hit », est considéré comme l'une des mécaniques fondamentales du jeu.

En règle générale, les champions peuvent gagner bien plus d'argent en portant le coup fatal qu'avec la simple génération d'or passive ou l'utilisation d'objets rapportant de l'or (quêtes). C'est pourquoi les objets destinés aux rôles axés sur le farming sont généralement plus chers que ceux destinés aux autres rôles.

Pour porter le coup fatal, les joueurs doivent utiliser des sorts infligeant des dégâts (attaques et compétences). Ils peuvent choisir le sort le moins coûteux et le plus rapide à utiliser, c'est-à-dire leur attaque de base ; ou une compétence, dont la plupart ont un temps de recharge plus long qu'une attaque de base et nécessitent souvent une ressource.

Réussir à porter le coup fatal exige un timing précis et une attention particulière aux sbires alliés, aux tourelles et/ou aux autres champions. Un sort infligeant plus de dégâts facilite évidemment cette tâche. Une vitesse d'attaque plus élevée peut également faciliter les coups fatals avec les attaques de base. Certaines compétences incitent à les utiliser pour le farming grâce à des mécaniques comme la réduction des temps de recharge, la récupération de mana, ou tout simplement parce qu'elles remplacent les attaques de base (par exemple, la compétence « Dévastation » de Karthus, la compétence « Crocs jumeaux » de Cassiopeia, la compétence « Déferlement de lames » d'Irelia, etc.). D'autres facteurs influencent le last-hit : la vitesse de déplacement des attaques de base ou des compétences, les projectiles, les temps de préparation, de canalisations et d'animation."""

tags = ["Gameplay", "Farming", "Bases"]

difficulty = "New Player"



addGuide(title, content, tags, difficulty)



title = "Farming - Laning"

content = """La phase de laning oblige les joueurs à interagir entre eux tout en se concentrant sur l'objectif commun de farmer. Utiliser un sort (y compris les attaques de base) sur un champion proche de ses sbires alliés ou se trouvant devant des sbires en mouvement aura pour conséquence que ces derniers cibleront automatiquement le champion ennemi intercepté et lui infligeront potentiellement des dégâts, jusqu'à ce que ce dernier soit suffisamment éloigné.

Lorsque deux joueurs farment de manière égale, aucun des deux ne possède d'avantage en ressources. Il est donc important pour un joueur en charge du farm d'être présent sur sa lane lorsque les sbires meurent et de donner le coup de grâce autant que possible, afin de maintenir un niveau de ressources égal à celui de son coéquipier lorsque les autres récompenses n'influencent pas les ressources acquises. Un joueur en charge du farm peut prendre du retard en expérience et en or s'il n'est pas présent sur sa lane et ne donne pas le coup de grâce, en raison de la mort des sbires ennemis face aux sbires alliés ou à la destruction d'une tourelle.

Une icône représentant le mot-clé « Élimination » (les éliminations et les objectifs épiques comme les monstres, les tourelles et les plaques de tourelle, entre autres) permet à un joueur de voie ou à son équipe de renverser l'équilibre, voire de compenser un déficit de farm (selon l'état de la partie). Un avantage significatif peut engendrer un effet boule de neige. À l'inverse, les champions ayant une meilleure progression que les autres peuvent obtenir la majeure partie, voire la totalité, de leur puissance en se concentrant exclusivement sur le farm en début et en milieu de partie."""

tags = ["Gameplay", "Farming"]

difficulty = "Average Player"

addGuide(title, content, tags, difficulty)



title = "Boucle de Farming"

content = """Une icône représentant le mot-clé « Sbire ». Les sbires ont un parcours prédéfini dans la partie. Deux champions adverses peuvent influencer ce parcours.

Une vague de sbires déferle sur chaque voie toutes les 30 secondes ; la puissance de cette vague détermine le rythme de la partie. Lorsqu'ils rencontrent la vague ennemie, les sbires s'arrêtent et s'attaquent mutuellement à portée jusqu'à ce que le sbire ciblé soit éliminé. Ensuite, le sbire survivant change de position jusqu'à attaquer le suivant, et ainsi de suite. À l'exception des super sbires, tous les autres sbires mettent un temps considérable à s'éliminer.

Un sbire de mêlée est plus fort qu'un sbire à distance.

Un sbire de siège est plus fort que les sbires de mêlée et à distance.

Selon la manière dont les sbires se rencontrent, de nombreuses combinaisons de combats sont possibles à tout moment, déterminant quels sbires meurent et à quelle vitesse. Par défaut, lorsque deux vagues de sbires de taille égale se rencontrent sans interruption, tous les sbires ciblent et attaquent en premier les sbires de mêlée adverses, car ce sont les premiers ou les plus proches.

Les champions des deux camps interagissent avec ces combats de sbires en infligeant des dégâts ou en exerçant un contrôle. Les actions entreprises par les deux joueurs de voie pour influencer les combats de sbires tout en tentant de porter le coup fatal et de défendre la structure à venir créent une boucle de farm dynamique. Cette boucle se réinitialise dès que deux vagues de sbires égales et opposées atteignent à nouveau le milieu exact d'une voie. Chaque champion présente une boucle de farm différente, et c'est un choix de conception délibéré.

Lorsque les sbires atteignent la portée d'attaque de la tourelle ennemie, cette boucle change. Les attaques de la tourelle infligent beaucoup plus de dégâts aux sbires que les attaques des sbires eux-mêmes, et elles infligent également un pourcentage spécifique des points de vie maximum de chaque type de sbire. Ce comportement aboutit à une boucle de farm beaucoup plus simple et statique, identique pour la majorité des champions en début de partie."""

tags = ["Gameplay", "Farming"]

difficulty = "Confirmed Player"

addGuide(title, content, tags, difficulty)



title = "Sbires"

content = """Pour chaque type de sbire ci-dessous, le nombre d'attaques de tourelle nécessaires pour l'éliminer est indiqué en premier, suivi des dégâts qu'il peut encaisser pour porter le coup de grâce. Les champions étant différents, il ne s'agit que de règles générales et non de calculs précis valables pour tous.

sbire de mêlée :

Attaques de tourelle : Il faut trois attaques de tourelle pour le tuer.

Cycle de dégâts : 2 attaques de tourelle → 1 attaque de champion

sbire lanceur de sorts :

Attaques de tourelle : Il faut deux attaques de tourelle pour le tuer.

Cycle de dégâts : 1 attaque de champion → 1 attaque de tourelle → 1 attaque de champion

sbire de siège :

Attaques de tourelle : Il faut huit attaques de tourelle (des tourelles extérieures) pour le tuer.

Cycle de dégâts : 7 attaques de tourelle → 1 attaque de champion

Les cycles de dégâts des sbires de siège sont très variables. Le cycle décrit ci-dessus est le cycle de base, sans tenir compte des interférences des sbires. Un autre exemple de cycle serait : 2 attaques de champion → 6 attaques de tourelle → 1 attaque de champion pour les champions ayant des dégâts d'attaque de base plus faibles. Les sbires de siège ayant une durée de vie bien supérieure à celle des sbires de mêlée et des lanceurs de sorts, ils sont plus susceptibles de subir des dégâts des sbires alliés, ce qui modifie le cycle de dégâts.



Les sbires progressent au fil de la partie, tandis que les dégâts des champions, provenant de différentes sources, augmentent à un rythme plus ou moins soutenu les uns par rapport aux autres et par rapport aux améliorations des sbires. Par conséquent, chaque champion a besoin de sources et d'un timing de dégâts différents pour farmer efficacement les sbires ennemis et empêcher l'ennemi de menacer les structures alliées au fur et à mesure que la partie avance. Concernant la boucle de farm sous tourelle, à mesure que les champions augmentent les dégâts de leur attaque de base (dégâts d'attaque + effets à l'impact), cette boucle peut varier considérablement. Les joueurs devront alors intégrer un nombre différent d'attaques et de compétences pour réussir à porter le coup de grâce aux sbires ciblés par une tourelle. Les coups critiques peuvent également influencer aléatoirement les boucles de farm, en particulier sous tourelle."""

tags = ["Présentation", "Farming"]

difficulty = "Average Player"



addGuide(title, content, tags, difficulty)

title = "Gestion des vagues de sbires"

content = """Une ligne de vagues est la ligne virtuelle qui traverse une voie, où un nombre quelconque (pair ou impair) de sbires se rencontrent et s'affrontent.

L'état des vagues décrit la position actuelle ou future des lignes de vagues sur la voie, en tenant compte de divers facteurs en cours de partie, tels que la différence actuelle du nombre et des points de vie des sbires, ainsi que l'activité ou l'absence des champions sur la voie. Les états des vagues déterminent le cycle de farm des champions à un moment donné de la partie et influencent la stratégie globale sur la carte.

Un joueur qui influence et contrôle délibérément l'état des vagues d'une voie par quelque moyen que ce soit effectue une gestion ou une manipulation des vagues. Les joueurs peuvent mettre en œuvre cette gestion dans le cadre de stratégies proactives ou réactives, selon la partie.

Par défaut, lorsque les sbires arrivent, s'affrontent et meurent, la ligne de vagues reste exactement au milieu de la voie, dans un état dit « neutre », car aucun camp n'avance ni ne recule.

Les champions peuvent influencer directement l'état neutre d'une vague de sbires en :

Infligeant plus de dégâts aux sbires ennemis que l'équipe adverse n'en inflige à ses propres sbires.

Modifiant la trajectoire des sbires ennemis (en pratique, seulement temporairement). Par exemple, en les incitant intentionnellement à attaquer le joueur et en les immobilisant pendant un certain temps ; en bloquant leur passage et en les forçant à faire un détour pour avancer ; en les ralentissant ou en les immobilisant ; etc.

Chaque vague de sbires suit une progression prédéfinie si les champions choisissent de ne pas interagir avec elle. Dans des circonstances normales, toute vague de sbires revient à l'état neutre tôt ou tard si aucune interaction n'est faite. Cela est dû au fait que les tourelles sont plus résistantes et infligent plus de dégâts que les sbires. Les vagues peuvent devenir déséquilibrées lorsqu'au moins un sbire a bénéficié d'effets spécifiques, ou lorsqu'une seule équipe invoque des super sbires.

Compte tenu de ce qui précède, il existe deux états de vague différents :

La poussée se produit lorsqu'un camp possède un avantage en points de vie et en nombre de sbires sur la ligne de vague.

Le gel se produit lorsqu'aucun camp ne possède un avantage en points de vie et en nombre de sbires sur la ligne de vague.

Plus précisément, la capacité de la ligne de vague à pousser est une fonction linéaire de l'avantage en points de vie et en nombre de sbires sur la ligne de vague (plus de sbires ou de points de vie signifient une plus grande puissance de poussée) par rapport à l'avantage temporel sur la ligne de vague (les sbires alliés arriveront plus rapidement sur la ligne de vague et la renforceront plus vite si elle est plus proche du Nexus d'un camp que de celui de l'autre). « Linéaire » car la vitesse de déplacement et les points de vie des sbires sur chaque voie sont linéaires et identiques pour les deux camps à chaque vague générée.

Les techniques de gestion des vagues reposent sur deux constats :

Les tourelles sont plus efficaces pour éliminer les sbires que les sbires eux-mêmes.

Le timing des vagues de sbires entrantes et leur influence sur la ligne de vague actuelle."""

tags = ["Gameplay", "Farming"]

difficulty = "Confirmed Player"


addGuide(title, content, tags, difficulty)


title = "Gestion des vagues de sbires"

content = """Fast Push

Un fast push, aussi appelée « bousculade », consiste à éliminer rapidement les sbires ennemis tout en conservant un avantage jusqu'à ce que tous (ou presque tous) les sbires alliés en vie puissent atteindre la tourelle suivante. Lors d'une poussée rapide, la vague de sbires avance sur une grande distance à chaque nouvelle vague.

Notez que les sbires alliés ayant acquis une tourelle (icône représentant le mot-clé « Tourelle ») ne peuvent pas changer de cible et donc pas attaquer les sbires ennemis, sauf si la tourelle est détruite. Si la poussée est parfaitement exécutée, aucun sbire allié n'est bloqué par les sbires ennemis et il est possible pour l'équipe alliée de ne manquer aucun sbire ennemi lorsque tous les sbires alliés finissent par mourir.

Pour un push efficace, il est crucial que le champion possède une capacité de nettoyage de vagues. Il s'agit de son efficacité à éliminer les vagues de sbires avec toutes ses compétences et attaques de base infligeant des dégâts, mesurée en secondes.

Slow Push

Un slow push consiste à infliger des dégâts aux sbires ennemis progressivement tout en conservant un avantage jusqu'à ce qu'un nombre suffisant de sbires s'accumulent et puissent atteindre la tourelle suivante. Lors d'une progression lente, la ligne de sbires avance légèrement à chaque vague entrante.

La vague résultante peut submerger une tourelle et dissuader les joueurs ennemis de l'attaquer, car elle peut infliger de lourds dégâts.

Freeze

Freeze manuellement la ligne de sbires consiste à la maintenir plus proche de la tourelle alliée suivante pendant au moins une vague de sbires, puis la suivante, en ne portant que le coup de grâce. Le gel est rompu lorsqu'un des sbires des deux camps parvient à avancer. Pendant un gel, la ligne de sbires n'avance ni ne recule de manière significative à chaque vague entrante.

Pour freeze la ligne de sbires, l'avantage en points de vie/nombre de sbires sur cette ligne doit rester proche de zéro. En pratique, plus la ligne de sbires est proche du Nexus d'un camp, plus il faut de sbires ennemis pour la freeze, car les renforts alliés arriveront plus vite. Pour compenser le coup de grâce, cet avantage doit également être légèrement négatif."""

tags = ["Gameplay", "Macro"]

difficulty = "Confirmed Player"


addGuide(title, content, tags, difficulty)



title = "Vue d'ensemble des Canalisations"

content = """Une canalisation est un trait de certaines capacités qui oblige le lanceur à rester occupé pendant un certain temps et à suspendre certaines de ses autres actions. Il existe deux types de canaux : normaux et chargés. Dans les deux cas, les canaux doivent être maintenus pour que l'utilisateur atteigne la puissance maximale possible sur leur(s) effet(s). Les canaux normaux ont une puissance constante, par exemple en provoquant un effet périodique ou en devant simplement être maintenus jusqu'à leur fin pour qu'une action se produise. Les canaux chargés sont activés pour augmenter la puissance du sort, puis réactivés pour les lancer à leur puissance résultante. Généralement, les canaux peuvent être interrompus par le lanceur ou par l'ennemi. Une icône représentant le mot-clé Contrôle des foules inhibant le contrôle des foules inhibant le casting.

Les canaux sont capables d'autoriser ou d'empêcher le lanceur d'effectuer certaines actions, notamment se déplacer, déclarer des attaques, lancer des capacités, utiliser des sorts d'invocateur ou activer des objets.

Pendant qu'un champion canalise, sa barre de santé affiche un contexte « Canalisation ». De plus, pour le joueur lui-même, le HUD affiche une barre avec le nom de la capacité canalisée en bas de l'écran pour l'indiquer. Pour les chaînes normales, la barre de diffusion précise le temps restant de la chaîne et progresse de droite à gauche. Pour les canaux chargés, la barre de lancement indique la puissance de l'effet et progresse de gauche à droite."""

tags = ["Gameplay", "Mécaniques"]

difficulty = "Average Player"



addGuide(title, content, tags, difficulty)


title = "Intéruption de Canalisations"

content = """La plupart des canalisations peuvent être interrompues pour annuler complètement le sort. Le lanceur peut interrompre sa canalisation en effectuant certaines actions, selon le sort.

Toutes les canalisations sont interrompues par les effets suivants : Contrôle des foules (icône représentant le mot-clé Contrôle des foules), Aérien (icône représentant le mot-clé Aérien), Action forcée (icône représentant le mot-clé Action forcée), Silence (icône représentant le mot-clé Sommeil), Stase (icône représentant le mot-clé Stase), Étourdissement (icône représentant le mot-clé Étourdissement), Suspension (icône représentant la suspension) et Suppression (icône représentant la suppression). Ces effets de contrôle des foules empêchent de lancer des sorts et interrompent donc les canalisations, tout en empêchant leur lancement. Perturbation (icône représentant le mot-clé Perturbation) est une forme spéciale de contrôle des foules qui interrompt spécifiquement les canalisations.

Les canalisations de mouvement, ou celles qui obligent le lanceur à se déplacer (par une ruée, un clignotement ou d'autres formes de mouvement), sont également interrompues par Enracinement (icône représentant le mot-clé Enracinement) et Sol (icône représentant le mot-clé Sol). Cela peut varier au cas par cas, selon le sort.

Les canalisations d'objectif, ou celles qui nécessitent que le lanceur soit hors combat, sont également interrompues lorsqu'il subit des dégâts.

Il est possible de configurer les canalisations pour qu'elles ne soient pas interruptibles ; dans ce cas, aucun des effets de contrôle des foules mentionnés précédemment n'affectera leur état. Notez que l'entrée dans l'état « Mort » ou « Résurrection » annulera toutes les actions en cours, y compris les canalisations.

Les canalisations interrompues par une autre personne que l'utilisateur ne donnent généralement lieu à aucun remboursement de coût ou de temps de recharge, sauf indication contraire. Les canalisations interrompues par l'utilisateur lui-même peuvent lui permettre de bénéficier d'un remboursement de coût ou de temps de recharge."""

tags = ["Gameplay", "Mécaniques"]

difficulty = "Average Player"



addGuide(title, content, tags, difficulty)


title = "Vue d'ensemble de la Jungle"

content = """Sur les cartes à plusieurs voies, la jungle désigne les zones situées entre les voies, à l'exclusion des bases des équipes. Elle se caractérise par une absence de visibilité ou un brouillard de guerre dense. Les créatures neutres (non agressives sauf si elles sont attaquées) sont appelées « Monstres ». Les monstres vivent dans la jungle, et un monstre ou un groupe de monstres à un endroit précis de la carte est appelé un camp.

Le rôle du jungler comprend trois responsabilités spécifiques. Celles-ci contrastent avec celles des joueurs de voie, dont le but principal est de farmer les sbires et de défendre les structures de leur voie en début de partie.

Farmer la jungle, c'est-à-dire éliminer les camps de monstres.

Avoir accès au sort d'invocateur « Châtiment » pour sécuriser des objectifs de monstres épiques, bénéfiques à toute l'équipe (Grulle du Néant, Héraut de la Faille, Baron Nashor et Drake de la Fosse aux Dragons). Enfin, en raison de l'étendue de la jungle, elle contribue généralement à l'assistance et à l'influence des voies."""

tags = ["Gameplay", "Macro", "Bases"]

difficulty = "New Player"


addGuide(title, content, tags, difficulty)



title = "Bases de la Jungle"

content = """La raison d'être du jungler est d'optimiser la répartition des ressources. La jungle regorge d'or et d'expérience, obtenus en éliminant les monstres qui apparaissent et réapparaissent à des endroits précis de la carte. Si un joueur se consacre à l'accumulation de ces ressources, les joueurs des voies peuvent en collecter davantage, au lieu de les partager avec un coéquipier. C'est particulièrement important pour les joueurs en solo lane, qui peuvent potentiellement obtenir le plus d'or et d'expérience grâce aux monstres de l'équipe.

La structure de la carte favorise naturellement l'acquisition de ressources en empruntant des chemins prédéfinis, appelés « pathing », car certains camps sont plus proches les uns des autres et/ou certains camps peuvent être prioritaires. Le jungler ne pouvant se positionner que près d'une moitié de la carte à la fois, ce pathing détermine également les voies et les objectifs situés dans sa zone d'influence immédiate. Minimiser le temps et les ressources consacrés au nettoyage des camps est essentiel pour un jungler afin de pouvoir prioriser les camps suivants, les combats, les autres objectifs et la pression générale sur l'équipe ennemie. Le farm des camps est généralement équilibré pour pouvoir être effectué par cycles, tandis que les champions et les monstres gagnent en puissance au fil de la partie. Les junglers en avance pourront faire tourner les monstres beaucoup plus rapidement, ce qui leur permettra de gagner du temps entre la destruction des camps et leur réapparition, et de farmer le cycle suivant plus vite.

Le jungler, comme tout rôle mobile, peut initier des embuscades contre ses ennemis pour les surpasser en nombre. Les embuscades contre les joueurs de lane sur les voies sont appelées ganks, et le manque de vision naturelle dans la jungle les facilite grandement. Les joueurs de lane doivent donc être vigilants et éviter les ganks grâce à une bonne vision et un contrôle de zone, ou s'en défendre par divers moyens, comme le contre-gank.

Enfin, et surtout, l'accès à une icône représentant Smite en tant que jungler leur confère un avantage certain pour éliminer les monstres de la jungle par rapport aux joueurs de lane, ainsi qu'un contrôle sur les objectifs épiques importants liés aux monstres et sur le jeu."""

tags = ["Gameplay", "Macro", "Bases"]

difficulty = "New Player"


addGuide(title, content, tags, difficulty)


title = "Combats dans la Jungle"

content = """Le farm, ou « clearing », d'un camp se fait dans la zone d'effet de chaque camp, indiquée par un cercle autour du camp lors du début du combat avec ses monstres. En dehors de cette zone, les monstres s'impatientent et finissent par régénérer automatiquement les dégâts subis avant de retourner à leur position initiale (réinitialisation).

Pendant un combat, l'attaquant peut créer une fenêtre de timing pour éviter les dégâts en s'éloignant du monstre avant qu'il ne prépare une attaque, tout en pouvant potentiellement riposter. Un champion à distance peut le faire plus souvent, car il peut attaquer à une portée supérieure à celle des monstres. En règle générale, les grands monstres peuvent se déplacer ou attaquer plus lentement (ou les deux) que la plupart des champions au fil de la partie.

Les monstres attaqueront toujours le champion le plus proche, qu'il les voie ou non. Un changement de cible peut alerter une équipe de la présence d'un ennemi à proximité. Les monstres tenteront de suivre une cible jusqu'à une icône représentant le mot-clé Pinceau, et n'« oublieront » pas immédiatement qu'un attaquant s'y est caché."""

tags = ["Bases"]

difficulty = "New Player"


addGuide(title, content, tags, difficulty)


title = "Objets de la Jungle"

content = """Afin d'inciter les junglers à farmer les camps de manière plus efficace que les laners, ils disposent d'objets de jungle exclusifs et essentiels. Ces objets garantissent également que les laners ne gagnent pratiquement rien à farmer les camps plutôt que les sbires de leur lane, surtout en début de partie. À l'inverse, les junglers gagnent beaucoup moins d'expérience en farmant les lanes grâce à leur objet de jungle.

Sbires de la lane.

bébé Marchevent.

jeune Piétineur.

chiot Griffe-Brûlée.

Acheter un objet de jungle invoque le familier correspondant pour aider le jungler à nettoyer les camps en infligeant des dégâts importants et en restaurant sa santé et son mana. Pour une efficacité optimale, l'objet de jungle doit être acheté dès le début de la partie, car il permet au jungler d'obtenir davantage de primes en or et en expérience pour l'élimination des camps de la jungle, ainsi que de nourrir son familier avec des friandises pour chaque gros monstre tué, ce qui lui confère certains bonus. Le familier peut évoluer à certains seuils de friandises pour octroyer au jungler un puissant bonus permanent, spécifique à son type, et débloquer l'accès aux améliorations de Châtiment : Châtiment déchaîné pour la première évolution et Châtiment primordial pour l'évolution finale.

En mode Classique 5v5 et en Faille de l'invocateur, ces seuils d'évolution sont respectivement de 20 et 40 friandises."""

tags = ["Bases", "Objets"]

difficulty = "New Player"


addGuide(title, content, tags, difficulty)


title = "Objets de la Jungle"

content = """Afin d'inciter les junglers à farmer les camps de manière plus efficace que les laners, ils disposent d'objets de jungle exclusifs et essentiels. Ces objets garantissent également que les laners ne gagnent pratiquement rien à farmer les camps plutôt que les sbires de leur lane, surtout en début de partie. À l'inverse, les junglers gagnent beaucoup moins d'expérience en farmant les lanes grâce à leur objet de jungle.

Sbires de la lane.

bébé Marchevent.

jeune Piétineur.

chiot Griffe-Brûlée.

Acheter un objet de jungle invoque le familier correspondant pour aider le jungler à nettoyer les camps en infligeant des dégâts importants et en restaurant sa santé et son mana. Pour une efficacité optimale, l'objet de jungle doit être acheté dès le début de la partie, car il permet au jungler d'obtenir davantage de primes en or et en expérience pour l'élimination des camps de la jungle, ainsi que de nourrir son familier avec des friandises pour chaque gros monstre tué, ce qui lui confère certains bonus. Le familier peut évoluer à certains seuils de friandises pour octroyer au jungler un puissant bonus permanent, spécifique à son type, et débloquer l'accès aux améliorations de Châtiment : Châtiment déchaîné pour la première évolution et Châtiment primordial pour l'évolution finale.

En mode Classique 5v5 et en Faille de l'invocateur, ces seuils d'évolution sont respectivement de 20 et 40 friandises."""

tags = ["Bases", "Objets"]

difficulty = "New Player"


addGuide(title, content, tags, difficulty)


title = "Cycles de Jungle"

content = """Le niveau des monstres est calculé à partir du niveau moyen des champions des deux équipes au moment de leur apparition, à l'exception des monstres épiques qui progressent en fonction du temps de jeu. Plus leur niveau augmente, plus leur prime d'expérience, leurs points de vie et leurs dégâts augmentent également. Il est donc important, surtout en début de partie, que le jungler choisisse un cheminement lui permettant d'atteindre certains niveaux en nettoyant les camps le plus efficacement possible. Cela crée un cycle où les camps réapparaissent et sont nettoyés plus rapidement, permettant ainsi au jungler d'accumuler encore plus d'or et d'expérience.

Les primes des monstres varient ; cependant, (et en supposant que le jungler ne gagne pas encore d'expérience autrement que dans sa jungle), nettoyer le premier camp de la partie le fera toujours passer au niveau 2. Certains monstres, comme le Mini Krug (icône An) ou le Raptor (icône An), peuvent être moins importants à éliminer pour atteindre certains paliers de niveau, car leurs primes sont exceptionnellement faibles.

Il est évident que les champions mettent beaucoup plus de temps à nettoyer les camps en début de partie, et certains junglers peuvent perdre beaucoup de points de vie ou de temps s'ils affrontent les monstres seuls, même avec un objet de jungle. Pour pallier ce problème, le jungler peut demander un « leash » pour son premier camp, où les alliés contribuent aux dégâts infligés au camp afin qu'il soit pris plus rapidement. Cependant, cette stratégie n'est pas toujours optimale pour les laners, car ils risquent de perdre le contrôle de leur lane plus tôt. Les modifications d'équilibrage apportées aux camps de la jungle et aux objets de départ des junglers ont rendu le leash moins important au fil des ans, mais il reste une stratégie importante à employer dans certaines situations.

Sur l'icône représentant le mot-clé Faille de l'invocateur, les alliés assistants sont uniquement les laners des lanes du haut et du bas, car les sbires de la midlane arrivent bien plus tôt que ceux des lanes du haut et du bas par rapport à l'apparition des camps."""

tags = ["Gameplay", "Macro"]

difficulty = "Average Player"

addGuide(title, content, tags, difficulty)


title = "Respawn des Camps de la Jungle"

content = """Les camps actifs, y compris ceux présumés actifs, sont indiqués sur la mini-carte par une icône en forme de losange à leur emplacement précis. Si une équipe aperçoit un camp de monstres non épiques en cours de nettoyage (icône représentant le mot-clé « Vue »), l'icône « Actif » est remplacée par un compte à rebours de réapparition, qui calcule automatiquement le temps de réapparition. Si une équipe n'a pas aperçu le camp de monstres non épiques en cours de nettoyage, elle peut en repérer l'emplacement dans un certain laps de temps avant sa réapparition afin d'obtenir un compte à rebours précis :

60 secondes avant la réapparition pour les camps de Sentinelle bleue et de Ronce rouge (icône représentant la Ronce rouge) ;

10 secondes avant la réapparition pour les camps de Gromp, de Krug ancien, de Loup des ténèbres supérieur et de Raptor cramoisi (icône représentant le Raptor cramoisi).

Préciser l'emplacement des camps avant ces délais (respectivement pour chaque camp) ne fournira aucune information à l'équipe sur leur statut.

La destruction des camps de monstres épiques est annoncée globalement pour les deux équipes, même si elles n'ont pas vu la destruction. Le temps de réapparition exact est donc toujours calculé pour les deux équipes. Ce temps de réapparition précis, ainsi que les icônes représentant les camps de Sentinelles bleues et de Ronce rouge (si connues), sont affichés en haut de l'écran lorsque le tableau des scores est ouvert (par défaut : ↹ TAB ou O), en plus de la mini-carte.

Les temps de réapparition des camps de monstres non épiques sur la mini-carte proposent deux modes d'affichage pour une meilleure lisibilité.

Sablon : 60 secondes avant la réapparition du camp, l'icône du sablier est grisée. 10 secondes avant la réapparition, elle devient jaune.

Texte : Lorsque le tableau des scores est ouvert, un texte plus précis remplace le sablier. Le format est M:SS. 10 secondes avant la réapparition du camp, il devient jaune. Il est possible d'afficher en permanence des minuteurs textuels pour tous les camps sur la mini-carte, à la place des sabliers, via l'option « Activer les minuteurs de camp » dans Paramètres > Interface.

Les camps de monstres épiques affichent toujours des minuteurs textuels, avec le même contexte d'affichage que celui décrit précédemment. La durée des minuteurs est limitée à 2 minutes pour plus de clarté, ce qui s'affiche sous la forme « 2m+ ».

Le premier temps d'apparition de tous les camps de monstres non épiques est toujours calculé automatiquement pour les deux équipes, car il s'agit d'une règle du jeu et l'apparition a lieu simultanément des deux côtés de la carte."""

tags = ["Gameplay", "Macro"]

difficulty = "Average Player"




addGuide(title, content, tags, difficulty)


title = "Invade et counter-jungle"

content = """L'invasion consiste à pénétrer dans la moitié ennemie de la jungle dans le but d'obtenir des informations et, si elle est effectuée par un jungler, de potentiellement voler des camps. L'invasion peut fortement perturber la capacité du jungler adverse à gérer son propre camp, et l'équipe alliée peut utiliser les informations obtenues pour élaborer ses propres stratégies.

Le contre-jungling consiste à envahir la jungle adverse dans le but précis de voler des camps afin de compenser un déficit connu. Par exemple, si le jungler adverse a envahi la jungle ennemie et nettoyé le camp de raptors allié, le jungler allié peut riposter en envahissant la jungle adverse pour nettoyer un camp ennemi et potentiellement égaliser la situation.

L'invasion et le contre-jungling peuvent tous deux dégénérer en affrontements, les joueurs des voies venant parfois effrayer ou repousser les envahisseurs, ou encore aider le jungler adverse lors d'une escarmouche pour tenter de leur tendre une embuscade."""

tags = ["Gameplay", "Macro", "Counterplay"]

difficulty = "Confirmed Player"


addGuide(title, content, tags, difficulty)


title = "Le Ganking en Jungle"

content = """Le ganking consiste à tendre une embuscade à un ou plusieurs adversaires sur leur voie, dans le but de réaliser des éliminations. Bien que le ganking ne soit pas l'apanage des junglers, c'est l'une des principales actions attendues d'eux en début de partie, car ils ne sont pas limités à une voie particulière. Cette liberté de mouvement dans le brouillard de guerre de la jungle peut rendre leurs décisions parfois imprévisibles (bien que plus prévisibles que celles d'un support, qui peut se déplacer librement malgré son positionnement initial sur la voie du bas ; le jungler doit en effet aller farmer les camps à un moment donné).

La grande majorité des junglers performants disposent d'outils spécifiques pour ganker efficacement et être le principal facilitateur de leur équipe : un mélange de contrôle de foule, de capacités de déplacement et de dégâts explosifs.

Cependant, tous les junglers ne sont pas censés ganker fréquemment. Certains junglers tirent profit de la sécurité potentielle du farm en jungle plutôt que des lanes où leurs adversaires les contestent constamment, et sont plus efficaces pour nettoyer les camps que pour ganker, faute d'outils adéquats. Cela les transforme davantage en carry qu'en facilitateur, et divise les junglers en deux grandes catégories. Si un jungler possède d'excellentes statistiques de base et les outils nécessaires pour ganker en début de partie, et préfère ganker fréquemment pour donner l'avantage à son équipe, on le qualifie de « jungler ganker ». À l'inverse, si un jungler a intérêt à accumuler un maximum de ressources en gankant moins souvent, afin de devenir potentiellement un carry principal avec une avance considérable en ressources sur l'adversaire, on le qualifie de « jungler farmer ». Les deux stratégies sont valables, mais la préférence pour le « gank » par rapport au « farming » varie d'un champion à l'autre, et même d'une mise à jour d'équilibrage à l'autre."""

tags = ["Gameplay", "Macro"]

difficulty = "Average Player"



addGuide(title, content, tags, difficulty)


title = "Vue d'ensemble des camps de la Jungle"

content = """Le ganking consiste à tendre une embuscade à un ou plusieurs adversaires sur leur voie, dans le but de réaliser des éliminations. Bien que le ganking ne soit pas l'apanage des junglers, c'est l'une des principales actions attendues d'eux en début de partie, car ils ne sont pas limités à une voie particulière. Cette liberté de mouvement dans le brouillard de guerre de la jungle peut rendre leurs décisions parfois imprévisibles (bien que plus prévisibles que celles d'un support, qui peut se déplacer librement malgré son positionnement initial sur la voie du bas ; le jungler doit en effet aller farmer les camps à un moment donné).

La grande majorité des junglers performants disposent d'outils spécifiques pour ganker efficacement et être le principal facilitateur de leur équipe : un mélange de contrôle de foule, de capacités de déplacement et de dégâts explosifs.

Cependant, tous les junglers ne sont pas censés ganker fréquemment. Certains junglers tirent profit de la sécurité potentielle du farm en jungle plutôt que des lanes où leurs adversaires les contestent constamment, et sont plus efficaces pour nettoyer les camps que pour ganker, faute d'outils adéquats. Cela les transforme davantage en carry qu'en facilitateur, et divise les junglers en deux grandes catégories. Si un jungler possède d'excellentes statistiques de base et les outils nécessaires pour ganker en début de partie, et préfère ganker fréquemment pour donner l'avantage à son équipe, on le qualifie de « jungler ganker ». À l'inverse, si un jungler a intérêt à accumuler un maximum de ressources en gankant moins souvent, afin de devenir potentiellement un carry principal avec une avance considérable en ressources sur l'adversaire, on le qualifie de « jungler farmer ». Les deux stratégies sont valables, mais la préférence pour le « gank » par rapport au « farming » varie d'un champion à l'autre, et même d'une mise à jour d'équilibrage à l'autre."""

tags = ["Gameplay", "Macro"]

difficulty = "Average Player"



addGuide(title, content, tags, difficulty)




title = "Toplaners"

content = """Les joueurs de la voie du haut évoluent sur une voie isolée (dans le coin supérieur de la carte), et doivent être autonomes grâce à d'excellents duels en 1v1, un farm précis et une bonne gestion des vagues de sbires pour générer de l'or indépendamment, tout en minimisant leur vulnérabilité aux ganks. La plus grande distance entre les tours de la voie du haut (comparée à la voie du milieu) permet de geler la vague et de prolonger les échanges, ce qui rend les sur-avancées ou une mauvaise gestion des vagues particulièrement punitives. Les joueurs de la voie du haut choisissent généralement des bruisers ou des tanks résistants. Ils utilisent souvent Téléportation combinée à Flash ou Flash combiné à Embrasement. La plupart des champions joués sur la voie du haut sont des champions de mêlée infligeant des dégâts physiques. Les joueurs de la voie du haut sont généralement efficaces en split-push. Parmi les cinq positions, la gestion des vagues est primordiale sur la voie du haut. Le contre-picking est crucial, car les joueurs de la voie du haut choisissent souvent leurs champions en dernier lors de la draft afin d'exploiter les matchups avec des champions capables de sustain, de poke ou de gap closer. La connaissance des matchups est donc essentielle à cette position. La plupart des joueurs de la voie du haut utilisent les runes Conquérant ou Poigne de l'immortel. Leurs objets de départ sont soit la Lame de Doran combinée à une potion de soin, soit le Bouclier de Doran combiné à une potion de soin."""

tags = ["bases", "presentation"]

difficulty = "New Player"



addGuide(title, content, tags, difficulty)




title = "Junglers"

content = """Le jungler parcourt la jungle neutre de la carte, farmant les monstres pour gagner de l'or et de l'expérience, tout en gérant les ganks, le contrôle des objectifs et le contre-jungling. Ce rôle exige une excellente vision de la carte, une grande efficacité dans ses déplacements et une capacité d'adaptation pour priver le jungler adverse de ressources. Il utilise généralement Châtiment combiné à Flash. Le jungler a pour mission de sécuriser les monstres épiques comme les Dragons, les Larves du Néant, le Héraut de la Faille, le Baron et le Dragon Ancestral. La plupart des junglers sont des combattants au corps à corps, infligeant soit des dégâts magiques, soit des dégâts physiques. Le jungler dispose d'objets de départ spécifiques, parmi lesquels trois options : Jeune pousse de Piétineur de Mousse, Jeune pousse de Marchevent ou Chiot de Griffe Brûlante. Ces objets sont parfois combinés avec une Potion de Soin, mais certains junglers préfèrent économiser leur or pour des achats ultérieurs. Les ganks sont primordiaux pour ce rôle."""

tags = ["bases", "presentation"]

difficulty = "New Player"



addGuide(title, content, tags, difficulty)




title = "Midlaners"

content = """Les midlaners évoluent sur une voie solo au centre de la carte, ce qui leur confère un contrôle unique et une grande influence sur la partie. Ils jouent généralement des mages (à burst ou à contrôle) et des assassins qui excellent sur les voies solo grâce à leur capacité à nettoyer rapidement les vagues de sbires et à leur montée en puissance avec l'expérience. Leur position leur permet de se déplacer rapidement vers les voies latérales, de participer à des escarmouches dans la jungle ou de prendre des objectifs comme le Dragon et le Héraut de la Faille. Les midlaners privilégient la gestion des vagues de sbires pour obtenir la priorité sur leur voie, ce qui leur permet de se déplacer en toute sécurité vers la voie du haut ou du bas pour des ganks et mettre la pression. Ils farment efficacement sur cette voie courte tout en surveillant les déplacements du jungler ennemi pour éviter les ganks, et coordonnent souvent leurs invasions avec leur propre jungler. Lors des combats d'équipe, ils ciblent les carrys fragiles comme l'ADC adverse avec des dégâts explosifs ou contrôlent la zone avec du poke et du contrôle de foule. La plupart des midlaners sont des DPS à distance ou au corps à corps, infligeant des dégâts magiques. La plupart des midlaners utilisent soit Flash combiné à Embrasement, soit Flash combiné à Téléportation. La voie du milieu est la plus risquée en raison de la pression constante des junglers ennemis. Le roaming est l'une des compétences les plus importantes à ce poste."""

tags = ["bases", "presentation"]

difficulty = "New Player"



addGuide(title, content, tags, difficulty)




title = "AD Carries"

content = """Les ADC sont les principaux infligeant des dégâts physiques. Ils évoluent sur la voie du bas aux côtés d'un support (la seule voie duo du jeu). Leur force réside dans leur capacité à infliger des dégâts continus grâce à leurs attaques automatiques, dont la puissance augmente avec les objets améliorant les dégâts d'attaque, la vitesse d'attaque, les chances de coup critique et les effets à l'impact. Leur rôle est particulièrement efficace lors des combats d'équipe en milieu et fin de partie, où ils peuvent éliminer aussi bien les tanks que les champions fragiles s'ils sont bien protégés. Ils dépendent fortement de leur support pour la protection, l'engagement et le contrôle de la vision. Les ADC optent généralement pour le Saut éclair combiné à la Barrière. Ce sont généralement les champions les plus fragiles de la classe. Les ADC commencent généralement la partie avec la Lame de Doran et une Potion de soin. Tous les ADC utilisent le mana comme ressource. La plupart des ADC choisissent Tempo mortel comme rune."""

tags = ["bases", "presentation"]

difficulty = "New Player"



addGuide(title, content, tags, difficulty)




title = "Supports"

content = """Le rôle de support consiste à soutenir l'ADC et son équipe grâce à des capacités utilitaires et une vision. C'est le seul rôle du jeu dont les revenus ne proviennent pas du farm, mais plutôt des objets de support et des assistances. Les supports débutent la partie sur la voie duo, en bas de la carte. Ils font équipe avec l'ADC, privilégiant les assistances aux éliminations tout en contrôlant le rythme de la voie. Ce rôle exige une excellente connaissance de la carte et une grande adaptabilité tout au long de la partie. Les supports protègent l'ADC en neutralisant les menaces grâce à des contrôles de foule, des boucliers ou des soins, ce qui permet un farm et des échanges de coups sûrs. Ils dictent la dynamique de la voie du bas par des engagements ou des désengagements agressifs, déterminant souvent les conditions de victoire dès le début grâce à des choix de champions comme les tanks, les enchanteurs ou les mages. Ils se positionnent aux côtés de l'ADC pour menacer les ennemis et réagir rapidement, évitant un jeu passif qui leur fait perdre le contrôle. Les supports se déplacent souvent sur la voie du milieu lorsqu'ils ont du temps libre. Tout comme les junglers, les supports disposent d'un objet de départ spécifique appelé Atlas du Monde, acheté automatiquement au début de la partie. L'Atlas mondial est combiné avec soit deux potions de soin, soit une balise de contrôle. Tous les supports utilisent le mana comme ressource. Les supports choisissent généralement les runes Invocation d'Aery, Comète arcanique ou Réplique. Parmi les autres runes de support, moins courantes, on trouve Gardien et Augmentation glaciale."""

tags = ["bases", "presentation"]

difficulty = "New Player"



addGuide(title, content, tags, difficulty)






title = "Commandes et contrôles - Bases"

content = """League of Legends se joue principalement à la souris et au clavier. Le clic droit permet de déplacer son champion et d'attaquer automatiquement les ennemis à portée. Le clic gauche sert à sélectionner des unités, des compétences ou des éléments de l'interface.

Les compétences du champion sont assignées par défaut aux touches Q, W, E et R. Elles peuvent être lancées soit en cliquant sur l’icône correspondante, soit via les raccourcis clavier. La plupart des joueurs utilisent le mode de lancement rapide (smart cast) pour gagner en réactivité.

Les sorts d'invocateur sont assignés aux touches D et F. Les objets peuvent être activés à l’aide des touches numériques (1 à 7). La touche B permet de retourner à la base, tandis que la touche P ouvre la boutique.

La caméra peut être déplacée avec la souris sur les bords de l’écran ou à l’aide des touches directionnelles. La barre espace recentre la caméra sur le champion, ce qui est fortement recommandé pour les débutants."""
 
tags = ["Commandes", "Contrôles", "Interface", "Bases"]

difficulty = "New Player"

addGuide(title, content, tags, difficulty)







title = "Objectif du jeu - Conditions de victoire"

content = """L'objectif principal d'une partie de League of Legends est de détruire le Nexus ennemi, situé au cœur de la base adverse. Pour y parvenir, les joueurs doivent progresser à travers les lanes, détruire les tourelles ennemies et remporter des combats stratégiques.

La carte principale, la Faille de l'invocateur, est divisée en trois lanes : la toplane, la midlane et la botlane, ainsi qu'une jungle. Chaque lane est protégée par des tourelles qu'il faut détruire dans un ordre précis.

Les équipes gagnent un avantage en accumulant de l'or, de l'expérience et des objectifs neutres (dragons, Héraut de la Faille, Baron Nashor). Une bonne coordination et une prise de décision collective sont essentielles pour transformer ces avantages en victoire."""
 
tags = ["Objectifs", "Victoire", "Carte", "Bases"]

difficulty = "New Player"

addGuide(title, content, tags, difficulty)






title = "Rôles et positions - Introduction"

content = """Chaque équipe est composée de cinq joueurs, chacun occupant un rôle spécifique. La toplane accueille généralement des champions résistants ou capables de tenir seuls sur la durée. La midlane est souvent occupée par des champions infligeant beaucoup de dégâts ou capables de se déplacer rapidement sur la carte.

La botlane est composée de deux joueurs : le carry AD (ADC), chargé d'infliger des dégâts soutenus, et le support, dont le rôle est de protéger, soigner ou contrôler les ennemis. Le jungler évolue quant à lui dans la jungle, éliminant des camps de monstres et intervenant sur les lanes pour créer des opportunités.

Comprendre son rôle et ses responsabilités est fondamental pour progresser et jouer efficacement en équipe."""
 
tags = ["Rôles", "Lanes", "Gameplay", "Bases"]

difficulty = "New Player"

addGuide(title, content, tags, difficulty)





title = "Or et expérience - Progression"

content = """L'or et l'expérience sont les deux ressources principales permettant à un champion de devenir plus puissant. L'expérience est gagnée en restant à proximité des sbires ennemis lorsqu'ils meurent, ainsi qu'en éliminant des champions ou des monstres de la jungle.

Monter de niveau permet d'améliorer ses compétences et d'augmenter ses statistiques de base. L'or, quant à lui, sert à acheter des objets dans la boutique afin d'améliorer les performances du champion.

Un bon équilibre entre farming, participation aux combats et prise d'objectifs est essentiel pour maintenir une progression constante tout au long de la partie."""
 
tags = ["Économie", "Expérience", "Objets", "Bases"]

difficulty = "New Player"

addGuide(title, content, tags, difficulty)





title = "Vision et balises - Fondamentaux"

content = """La vision est un élément clé de League of Legends. Elle permet d'anticiper les déplacements ennemis, d'éviter les embuscades et de sécuriser les objectifs importants.

Les balises de vision (wards) peuvent être placées sur la carte pour révéler une zone pendant une durée limitée. Chaque joueur peut poser des balises grâce à la balise de vision incluse dans son inventaire.

Contrôler la vision autour des objectifs comme les dragons ou le Baron Nashor donne un avantage stratégique majeur. Même les joueurs débutants doivent prendre l'habitude de poser régulièrement des wards."""
 
tags = ["Vision", "Wards", "Stratégie", "Bases"]

difficulty = "New Player"

addGuide(title, content, tags, difficulty)
