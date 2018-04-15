require(alluvial)
degree = read.csv('graph2.csv')
colnames(degree)
library(dplyr)


alluvial(degree$Education_Level,degree$Education_Category, degree$Previous_Job_Title, degree$Current, freq= degree$Number, 
     alpha = 0.8,layer = degree$Previous_Job_Title == "Student",hide = degree$Number < 30,border=NA,
     col = ifelse( degree$Previous_Job_Title == "Student", "red",  
                   ifelse( degree$Previous_Job_Title == "Data Scientist", "green",  'lightskyblue')))


cols= c('Previous_Job_Title', 'Current', 'Education_Category', 'Education_Level' , 'Number')
colnames(dg2) = cols

ord <- list(NULL, NULL, order(dg2$Education_Category,count(dg2$Education_Category)), NULL)
alluvial(dg2$Education_Level,dg2$Education_Category, dg2$Previous_Job_Title, dg2$Current, freq= dg2$Number, 
         alpha = 0.8,layer = dg2$Previous_Job_Title == "Student",hide = dg2$Number < 30,border=NA,
         ordering= ord,
         axis_labels = c("Highest Education Level", "Highest Education Field", "Prev Job Title", "Current Job Title"),
         col = ifelse( dg2$Previous_Job_Title == "Student", "red",  
                       ifelse( dg2$Previous_Job_Title == "Data Scientist", "green",  'lightskyblue')))