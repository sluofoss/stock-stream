locals {
  #description   = "the folder which the data cron job code reside, the package should also be zipped there."
  #type          = string
  datacron_yfinance_folder       = "${path.module}/../../../../datacron/yahoo-finance"
    # pipeline //modules//yahoo-finance//datacron//tf-iaac//stock_2023
}