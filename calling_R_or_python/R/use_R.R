rm(list=ls())

args = (commandArgs(trailingOnly=TRUE))
if(length(args) == 2){
  i = as.numeric(args[1])
  outfile = args[2]
} else {
  cat('usage: Rscript use_R.R <i> <output tfile>\n', file=stderr())
  stop()
}

cat("Hello, world (stdout), i=", i, "\n") # This line goes to stdout. Next lines goes to outfile.

sink(file=outfile) # send stdout to outfile from now on

if (require("FITSio")) { # require() is like library(), but returns TRUE or FALSE
  print("Loaded package FITSio.")
} else {
  print("Failed to load package FITSio.")  
}

if (require("tidyverse")) {
  print("Loaded package tidyverse.")
} else {
  print("Failed to load package tidyverse.")  
}

cat(sep="", "Hello from the R job in process i=", i, ".\n")
cB58 = readFrameFromFITS("cB58_Lyman_break.fit") # use FITSio package
print(head(cB58))

cat("\n")
# To make the next tidyverse line work, uncomment it and use the posted
#   packages_FITSio_tidyverse.tar.gz
# file instead of packages_FITSio.tar.gz. Also change 
# "request_disk = 1MB" to "request_disk = 1GB" in myscript.sub.
mtcars %>% summarize(mean_mpg=mean(mpg), sd_mpg=sd(mpg)) # use tidyverse

sink() # stop sending stdout to outfile
