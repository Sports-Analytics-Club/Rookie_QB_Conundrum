## INSTALL PACKAGES ======
### you should have most of these packages, maybe not glue + here, but good to run this
### to install any that you don't have

packages <- c('dplyr', 'stringr', 'purrr', 'rvest', 'glue', 'here', 'readr')

installed_packages <- packages %in% rownames(installed.packages())
if (any(installed_packages == FALSE)) {
  install.packages(packages[!installed_packages])
}

invisible(lapply(packages, library, character.only = TRUE))

## FUNCTION =========
### not the most efficient way b/c I threw it together in just a few min., but given
### what we're scraping, it doesn't really matter

get_players <- function(letter) {

  # pages are indexed w/ an upper-case letter
  url <- glue::glue("https://www.pro-football-reference.com/players/{toupper(letter)}/")

  html <- read_html(url) # store html for later reference

  # create a tibble with information requested
  tib <- tibble(
    meta = html |> html_nodes('#div_players p') |> html_text(), # what the site shows
    position = stringr::str_extract(meta, "(?<=\\().+?(?=\\))"), # extract positions played
    is_qb = if_else(grepl('QB', position), 1, 0), # binary for if player is a qb
    year_span = stringr::str_squish(gsub('.*\\)','', meta)), # year span as shown on site
    start_year = as.numeric(gsub('-.*', '', year_span)), # starting year (as an integer)
    end_year = as.numeric(gsub('.*-', '', year_span)), # ending year (as an integer)
    slug = html |> html_nodes('#div_players a') |> html_attr('href'), # player slug
    full_slug = glue::glue("https://www.pro-football-reference.com{slug}") # full url address
  )

  return(tib)
}


## SCRAPE =========
### for-loops are inefficient in R; it is preferred to use a `purrr` mapping function
### here, we will use `map_dfr` so our results are appended together

players <- map_dfr(
  .x = letters,
  .f = function(letter) {

    message(glue::glue('Getting {letter}')) # just to track progress

    Sys.sleep(8) # SR seems to spin a wheel re: what sleep time you need for any given day

    # return empty result on an error so loop continues
    tryCatch({
      get_stuff(letter) |>
        mutate(iter = letter) }, # add which letter we're on for debugging if needed
      error = function(e) {}
    )

  }
)

## SAVE =========
### save data to repo using `here` instead of using raw paths

write_csv(players, here("data", "player_links.csv"))

