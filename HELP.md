** Portable Secured Station **

*Description*
Cette application composée essentiellement à partir du langage python, permet de stocker des données d'identité (clé privé et publique RSA) de manière sécurisée par chiffrement des données gâce aux lgorithmes AES et sha512. Vous pourrez donc transporter avec vous des données sensibles sans que personnes ne puisse les lire sans connaître le mot de passe de déchiffrement. Vous pouvez aussi rajoutez vos propres scripts dans le dossier Libs afin d'augmenter le nombre de commandes disponibles.

*Installation*
Exécutez l'installeur de cette manière pour l'installation:
    ./installer.sh local -> ne requiert pas les droits root, et permet une installation de l'App pour l'utilisateur concerné.
    Installation dans les dossiers: /home/$USER/.local/lib/PSS /home/$USER/.config/PSS 
    Fichier d'activation: /home/$USER/.local/bin/pss

    ./installer.sh global -> requiert les droits root, installe l'application pour tous les utilisateurs du système.
    Installation dans les dossiers: /usr/lib/PSS /var/lib/PSS
    Fichier d'activation: /usr/local/bin/pss
    Crée le rôle PssUser, seuls les membres de ce groupe pourront utiliser les commandes liées à l'application

*Desinstallation*
Executez: ./installer.sh remove global|local

*Avertissement*
Ce repos comporte de nombreuses failles de sécurité logicielles et cryptographiques, je recommande d'utiliser ce travail dans un cadre récréatif plutôt que professionnel. 