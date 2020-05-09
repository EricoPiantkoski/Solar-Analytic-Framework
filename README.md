# Solar-Analytic-Framework

This project is my Final Project by the State University of Mato Grosso (UNEMAT).

Its function is to inform a user of an Off-Grid solar energy system whether or not there is a need for energy savings. It uses two databases (BDMEP and INPE) and creates an empirical model of that.

The databases of the Meteorological Database of Teaching and Research (BDMEP) of the National Institute of Meteorology (INMET), return important data on Insolation (photoperiod) considered. This information is provided in hours for the user's respective location through physical stations.
For more information about BDMEP, visit:
http://www.inmet.gov.br/portal/

The databases of the National Institute for Space Research (INPE) are provided by the Laboratory for Modeling and Studies of Renewable Energy Resources (LABREN) through the Atlas Brasileiro de Energia Solar. The relevant data used for this project consist of direct and diffuse radiation (in KWh / m²).
For more information about INPE and its project Atlas Brasileiro de Energia Solar, access:
http://labren.ccst.inpe.br/atlas_2017.html#mod

Both databases are used to accurately predict radiation. Such data are compared to the user's energy consumption and then it can be measured whether he needs to save energy or not.

The project uses different sensors to know the user's location and to measure their consumption using ESP8266, a development board, which sends such data to a remote server, using Micropython. The information is presented on a web page.

It is hoped that this work can corroborate future research using the most diverse fields of Computer Science.

