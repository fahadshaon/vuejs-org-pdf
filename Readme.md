# Vuejs.org PDF

Project to create PDF version of vuejs.org guilds

## Requirements

- `git`
- `npm`
- `virtualenv`
- `wget`

## Run

Intialize first

    ./run.sh init

It will

- Clone the `vuejs.org` repository into `build` folder
- Install `vuejs.org` project dependencies with `npm`
- Build `vuejs.org` using `npm`
- Create virtual environement for this project using `virtualenv`
- Install this projects dependencies
- Copy css, js, and images into `build/dist`


Install the `wkhtmltopdf` package, only works only in **ubuntu**

    ./run.sh install_wkhtmltopdf

Default version of wkhtmltopdf does not have attached qt, so the output
is suboptimal

Now build the pdf and html file

    ./run.sh build

