# PSL Robocup 2022 - 2023 : Informatique embarquée
Collection de codes pour microbit permettant de faire fonctionner les différents organes du robot.
<h1>Configuration d'un robot</h1>
<h2>Configuration des moteurs MX12</h1>
Plusieurs registres sont à modifier sur chaque MX12.
Ces registres peuvent être changés à l'aide du logiciel dynamixel-wizard :
<a href="https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_wizard2/#software-installation"> https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_wizard2/#software-installation</a>
<br>
Il est nécessaire d'avoir un module de communication entre l'ordinateur et les MX12.
<h3>Identifiants de moteurs</h3>
Pour changer l'identifiants des moteurs, il suffit de changer le registre ID dans dynamixel wizard.
Les identifiants des moteurs doivent être réglés dans l'ordre indiqué par l'image suivante : 
<p float="left">
  <img src="./img-readme/moteurs.jpg" width="30%" height="30%" />
  <img src="./img-readme/dynam-id.png" width="50%" height="50%" />
</p>
<h3>Réglage de return delay time</h3>
Une fois l'identifiant changé, refaites un scan.
Le registre <b>Return Delay Time</b> doit être réglé à <i>100 μs</i>.
Il faut mettre 50 sur l'interface, l'unité étant de <i>2 μs</i>.
<p float="left">
  <img src="./img-readme/wizard-delay.png" width="60%" height="60%" />
  <img src="./img-readme/delay-time.png" width="18%" height="18%" />
</p>
<h2>Configuration de l'identifiant du robot et du canal de transmission</h2>
Depuis l'IDE en ligne <a href="https://python.microbit.org/v/3">https://python.microbit.org/v/3</a>,
ouvrez le fichier <i>projet-code-robot.hex</i> présent dans le dossier <it>Robot</it> ou bien importez
un par un par chaque module du dossier <i>Robot</i>. 
Par défaut l'identifiant du robot est égal à 0 et le canal de transmission à 10.
Pour les modifier, changer les valeurs de <i>idRobot</i> et de <i>groupe_canal</i>
dans le fichier <i>main.py</i>.
<h2>Téléversement vers la microbit</h2>
Toujours sur l'IDE en ligne <a href="https://python.microbit.org/v/3">https://python.microbit.org/v/3</a>,
avec <i>projet-code-robot.hex</i> d'ouvert et la microbit branchée sur votre ordinateur,
appuyer sur <i>Send to micro:bit</i>.
<h1>Structure du projet</h1>
Tous les codes relatifs au robot sont dans le répertoire Robot.
Tous les codes relatifs à l'émetteur sont dans le répertoir PC-Coach. 
<h2>main.py</h2>
Décrit le comportement du robot à l'aide des différents modules.

<h2>refpin.py</h2>
Référence les pins utilisés avec des noms explicites.

<h2>drible.py</h2>
Module pour le contrôle du moteur de drible.

<h2>tircharge.py</h2>
Module où sont définis les fonctions de commande de charge du condensateur
et de commande de tir.

<h2>mx12.py</h2>
Module pour le contrôle des moteurs mx12.


<h2>telecom.py</h2>
Module pour la communication radio avec le coach

<h2>test.py</h2>
Description d'un routine de test permettant de valider le bon fonctionnement du robot
