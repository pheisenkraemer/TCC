# TCC
Here I disclose the algorithms I developed for my final graduation report

The objective of this work was to develop a methodology to analyse the impacts of the Electric Vehicles Charging Stations in Brazilian distribution systems, 
aiming to serve as a basis for the planning and expansion of the Electrical Systems in Brazil.

The method used in this work is based on the Monte Carlo Simulation. In general, this method is characterized by the repetition of the simulations and the 
sampling of the input variables in order to generate different scenarios for analysis. 
In this work, the Factors that were subject to randomness were the loadshapes of consumers and the bars where the Electric Vehicles Charging Stations
are allocated. The implementation of the methodology is carried out through the py-dss-interface library and the OpenDSS software. 

The main measurements in this study to evaluate the different cenarios are related to technical losses, voltage levels and network loading.
The analysis consists in evaluating how the increase in the penetration level of Charging stations affects these three factors.
This assessment uses temporal power flow analysis, which is responsible for solving the circuit for a defined period of time. 
Finally, impacts are measured and illustrated using graphical tools to promote a deeper analysis and discussion of the results.
