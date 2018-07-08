library(grid)
library(stringr)
library(scales)
library(stringi)
library(plyr)

data <- read.csv('rating_data.csv')
num_participants <- nrow(data)

group_midpoints <- function(g) {
  cumsums = c(0, cumsum(g$Freq))
  diffs = diff(cumsums)
  pos = head(cumsums, -1) + (0.5 * diffs)
  return(data.frame(value=g$value, pos=pos, Freq=g$Freq))
}

chi_squared_multiple_test <- function(vector_one, vector_two, fileName){
	combs <- expand.grid(vector_one,vector_two)
	combs <- data.frame(lapply(combs, as.character), stringsAsFactors=FALSE)
	results = data.frame( Row=rep(0, dim(combs)[1]), 
		Column=rep(0,dim(combs)[1]), 
		Chi.Square=rep(0,dim(combs)[1]), 
		df=rep(0,dim(combs)[1]),
		p.value=rep(0,dim(combs)[1]))

	for (i in 1:dim(combs)[1]){
			test <- chisq.test( data[[combs[[1]][i]]], data[[combs[[2]][i]]])

			results[i, ] = c(combs[[1]][i]
	                    , combs[[2]][i]
	                    , round(test$statistic,7)
	                    ,  test$parameter
	                    ,  round(test$p.value, 7)
	                    )
	}

	results$p.value <- as.numeric(results$p.value)
	adjusted<-p.adjust(results$p.value,method="bonferroni") #adjust using conservative bonferroni method (Holm's used by Robillard)
	results$p.value<-adjusted

	for (i in 1: dim(results)[1]){
		if (results[i,]$p.value < 0.05){
			cat(sprintf("\\pgfkeyssetvalue{%s_%s_p_value}{%0.6f}\n",
					combs[[1]][i],
					combs[[2]][i],
					results[i,]$p.value,
					'',
					sep='')
				)
		}
	}
	write.csv(results, fileName)
}


####################Occupations#############################
#aggregate occupations
levels(data$OCCUPATION)[match("Academic Researcher",levels(data$OCCUPATION))] <- "Researcher"
levels(data$OCCUPATION)[match("Industrial Researcher",levels(data$OCCUPATION))] <- "Researcher"
levels(data$OCCUPATION)[match("Graduate student",levels(data$OCCUPATION))] <- "Student"
levels(data$OCCUPATION)[match("Undergraduate student",levels(data$OCCUPATION))] <- "Student"
levels(data$OCCUPATION)[match("Freelance developer",levels(data$OCCUPATION))] <- "Professional Developer"
levels(data$OCCUPATION)[match("Industrial developer",levels(data$OCCUPATION))] <- "Professional Developer"


##############################correlations#####################################
background=c("OCCUPATION",
	"EXPERIENCE")

metrics=c(
 	"POPULARITY",
 	"RF",
 	"LMD",
 	"PERFORMANCE",
 	"SECURITY",
 	"IRT",
 	"ICT",
 	"BC",
 	"LDSO",
 	"APPROACH")

##### chi squared between backround and individual metrics + overall approach eval
chi_squared_multiple_test(background, metrics, 'background_ratings_chi_sq.csv')


##### spearman correlation between metrics #########
# don't know --> 0
# never --> 1
# rarely --> 2
# occasionally --> 3
# frequently --> 4
correlation_data = data[metrics]


#convert to numeric
correlation_data[,metrics] = as.numeric(as.character(unlist(correlation_data[,metrics])))

correlations = cor(correlation_data, method="spearman")
write.csv(correlations, 'correlations_spearman.csv')

row_names=rownames(correlations)

for (i in 1:dim(correlations)[1]){
	for (j in 1:i){
		if(i!=j && correlations[i,j] > 0.5){
			obs1= row_names[i]
			obs2= row_names[j]
			test <- cor.test(correlation_data[[obs1]], correlation_data[[obs2]], method="spearman")
			cat(sprintf("\\pgfkeyssetvalue{%s_%s_correlation}{%0.2f}\n",
				obs1,
				obs2,
				round(correlations[i,j],digits=2),
				'',
				sep='')
			)
			cat(sprintf("\\pgfkeyssetvalue{%s_%s_p_value}{%0.6f}\n",
				obs1,
				obs2,
				round(test$p.value,digits=6),
				'',
				sep='')
			)
		}
	}
}
