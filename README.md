# projet-robocup
Codes permettant de faire fonctionner les robots du projet Saphire Robocup 2022-2023 .

<h1>Configuration d'un robot</h1>
<h2>Configuration des moteurs MX12</h1>
Plusieurs registres sont à modifier sur chaque MX12.
Ces registres peuvent être changés à l'aide du logiciel dynamixel-wizard :
<a href="https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_wizard2/#software-installation"> https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_wizard2/#software-installation</a>
<br>
Il est nécessaire d'avoir un module de communication entre l'ordinateur et les MX12.
<h3>Identifiants de moteurs</h1>
Les identifiants des moteurs doivent être réglés selon l'image suivante :  
<img src="./img-readme/moteurs.jpg" width="80%" height="80%">
<h3>Configuration de l'identifiant du robot et du canal de transmission</h3>
Par défaut l'identifiant du robot est égal à 0 et le canal de transmission à 10.
Un menu permettant de configurer l'identifiant du robot et le canal de transmission
est disponible.
Pour accéder à ce menu il suffit d'appuyer sur le bouton b.
Pour changer la sélection, il faut appuyer sur le bouton b.
Pour confirmer un choix, attendre 5 secondes sans rien toucher.
En-dehors du menu, la ligne la plus haute indique l'identifiant du robot
et la ligne juste en-desssous, le canal de transmission.

<h1>Structure du projet</h1>
Tous les codes relatifs au robot sont dans le répertoire Robot.
Tous les codes relatifs à l'émetteur sont dans le répertoir PC-Coach. 
<h2>main.py</h2>
Décrit le comportement du robot à l'aide des différents modules

<h2>menu.py</h2>
Module permettant à l'utilisateur
d'accéder à un menu où il peut modifier
l'identifiant du robot et le canal de transmission.

<h2>refpin.py</h2>
Référence les pins utilisés avec des noms explicites.

<h2>tircharge.py</h2>
Module où sont définis les fonctions de commande de charge du condensateur
et de commande de tir.

<h2>mx12.py</h2>
Module pour le contrôle des moteurs mx12


<h2>telecom.py</h2>
Module pour la communication radio avec le coach
