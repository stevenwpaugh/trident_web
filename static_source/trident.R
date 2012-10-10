.getTridentemail <- function () {
if (!exists(".Tridentemail")){
.Tridentemail <<- readline("Please enter your Trident registered email address: \n")
}
}

tridentinstall <- function(x){
if (x == "TridentAPI"){
.getTridentemail()
download.file(paste("http://pled01.stjude.org/TridentAPI_0.1.tar.gz?email=", .Tridentemail, sep=""), paste(getwd(), "TridentAPI_0.1.tar.gz", sep="/"), mode="wb")
install.packages("XML")
install.packages("png")
install.packages(paste(getwd(), "TridentAPI_0.1.tar.gz", sep="/"), repos=NULL, type="source")
unlink(paste(getwd(), "TridentAPI_0.1.tar.gz", sep="/"))
}
if (x != "TridentAPI"){
cat("ERROR: An invalid package name was specified\nPlease try again\nSee http://pled01.stjude.org/api/ for more details.\n")
}
}

