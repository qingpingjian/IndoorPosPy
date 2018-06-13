*** 该目录同级脚本需要在tensorflow环境中运行，并且需要运行的时间比较长，最好在服务器上的虚拟机中运行。***

Attribute Information:

Attribute 001 (WAP001): Intensity value for WAP001. Negative integer values from -104 to 0 and +100. Positive value 100 used if WAP001 was not detected. 
.... 
Attribute 520 (WAP520): Intensity value for WAP520. Negative integer values from -104 to 0 and +100. Positive Vvalue 100 used if WAP520 was not detected. 
Attribute 521 (Longitude): Longitude. Negative real values from -7695.9387549299299000 to -7299.786516730871000 
Attribute 522 (Latitude): Latitude. Positive real values from 4864745.7450159714 to 4865017.3646842018. 
Attribute 523 (Floor): Altitude in floors inside the building. Integer values from 0 to 4. 
Attribute 524 (BuildingID): ID to identify the building. Measures were taken in three different buildings. Categorical integer values from 0 to 2. 
Attribute 525 (SpaceID): Internal ID number to identify the Space (office, corridor, classroom) where the capture was taken. Categorical integer values. 
Attribute 526 (RelativePosition): Relative position with respect to the Space (1 - Inside, 2 - Outside in Front of the door). Categorical integer values. 
Attribute 527 (UserID): User identifier (see below). Categorical integer values. 
Attribute 528 (PhoneID): Android device identifier (see below). Categorical integer values. 
Attribute 529 (Timestamp): UNIX Time when the capture was taken. Integer value. 

Citation in BibTex:
@inproceedings{torres2014ujiindoorloc,
  title={UJIIndoorLoc: A new multi-building and multi-floor database for WLAN fingerprint-based indoor localization problems},
  author={Torres-Sospedra, Joaqu{\'\i}n and Montoliu, Ra{\'u}l and Mart{\'\i}nez-Us{\'o}, Adolfo and Avariento, Joan P and Arnau, Tom{\'a}s J and Benedito-Bordonau, Mauri and Huerta, Joaqu{\'\i}n},
  booktitle={2014 International Conference on Indoor Positioning and Indoor Navigation (IPIN)},
  pages={261--270},
  year={2014},
  organization={IEEE}
}

Statistics:
(1) 独立的 SPACEID不能作为字典中的键值，不同的楼以及相同的楼中不同的楼层具有相同的Space编号，
