# Solar-Analytic-Framework

This project was developed at the State University of Mato Grosso (UNEMAT) as a monograph for completion of the Computer Science course. Through a development circuit in the IoT scope, we use information from the user's electrical grid, added to local solar radiation prediction information, to inform an off-grid electrical system user if there is a need for energy savings.

The databases of the Meteorological Database of Teaching and Research (BDMEP) of the National Institute of Meteorology (INMET), return important data on Insolation (photoperiod) considered. This information is provided in hours for the user's respective location through physical stations. For more information about BDMEP, visit: http://www.inmet.gov.br/portal/

The databases of the National Institute for Space Research (INPE) are provided by the Laboratory for Modeling and Studies of Renewable Energy Resources (LABREN) through the Atlas Brasileiro de Energia Solar. The relevant data used for this project consist of direct and diffuse radiation (Wh/m²). For more information about INPE and its project Atlas Brasileiro de Energia Solar, access: http://labren.ccst.inpe.br/atlas_2017.html#mod

Both databases are used to accurately predict radiation. Such data are compared to the user's energy consumption and then it can be measured whether he needs to save energy or not.

The project uses different sensors to measure energy consumption and acquisition and, through ESP8266, sends this data to a remote server, using the Micropython language. The server works the data and combines it in real time with the user's specific solar radiation predictions, returning it to the ESP8266. The information is then presented on a web page, hosted on the ESP8266 itself.

Very soon an article containing all the implementation and development details, as well as all the materials and methods used, will be made available in academia. When this happens, this description file will be updated for more information. It is hoped that this work can support future research using the most diverse fields of Computer Science.

