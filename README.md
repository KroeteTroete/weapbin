# weapbin
Weapbin is a script used for modifying the weapons.bin file of Galaxy On Fire 2.
The weapons.bin file of GOF2 stores the coordinates of every hardpoint (Primary weapon, secondary weapon, turret and engine) of every ship. The file can be edited by manually searching for the ship ID and total amount of hardpoints of a ship inside a hex editor and then modifying the coordinate-bytes. This script creates a JSON file for every ship, placing it's hardpoint information into it. This not only makes it easier to modify existing coordinates of hardpoints, but also adding completely new hardpoints. Once the modifications have been made, weapbin can build and new functional weapons.bin file.

# How to use - Extracting
The weapons.bin file can be found in the data/bin folder inside the GOF2 directory. Place the weapons.bin file into the same folder as the weapbin.py script. Open the folder containing both files in CMD or Powershell and type: "python .\weapbin.py extract". You will find around 40 to 43 (the amount will depend on which version of the game you're modifying) JSON files inside your folder. 

# How to use - Finding the right Ship ID
To find the .json file for the ship you're trying to modify you can use the name of it's 3D model. The 3D models can be found in the data/assets/main/3d/meshes/ships folder. To open the .aem files you can use <a href="http://3doc.i3dconverter.com/">i3D</a> or Pb-207's <a href="https://github.com/Pb-207/AemConvertor">AemConvertor</a>. For example:
The Inflict 3D model is called "ship_005_terran.aem", so it's ID is 5. The corresponding .json file created by weapbin is called "ship_5.json".

# Adding new hardpoints
If your goal is not to move existing hardpoints, but adding a new one, you can copy the section of one of the hardpoints (e.g a primary weapon), paste them after the last one of the same type, change the hardpoint number accordingly (e.g if you copied the values of primary_3_key: primary_3, your new hardpoint should be called primary_4_key: primary_4) and enter the coordinates. Then to back to the top of the .json file and increase the "total" value (the total amount of hardpoints) by the amount of hardpoints you added. If you're adding a primary, turret or secondary, your hardpoint wond't work by only modifying weapons.bin. You also have to edit the ship's stats (located in the ships.bin file) in that case, which can be done using Exilium's <a href="https://mega.nz/#F!nZUEGSLT!_jh8vQzG5T4mhTe7sDLcpg>GOF-Modder</a>. If you're adding a new primary weapon, secondary weapon or turret to a ship, you will have to change it's corresponding ship-stat in ships.bin. However, this isn't neccessary for adding engines.

# How to use - Building
Once you've made your modifications, open up your weapbin folder in CMD or Powershell again and type "python .\weapbin.py build". This will create a new file called "weapons_built.bin". Place this file in your data/bin folder to replace the vanilla/unmodified weapons.bin file.
