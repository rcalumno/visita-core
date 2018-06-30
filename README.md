# _visita-core_
## _Proyecto para el curso de modelo de datos_
Integrantes
- Cristina Suarez
- Veronica Vega
- Hugo Bonini
- Roberto Chasipanta

## Creaci&oacute;n del ambiente virtual

```commandline 
python -m venv visita_core

- windows /cmd
visita_core\Scripts\activate.bat

- unix
source tutorial-env/bin/activate 
```


## Instrucci&oacute;n necesaria para la covertura
```commandline
coverage run -m src.odd_number --source=_test_,src _test_/test_math.py 

```


##
```commandline
mongo --authenticationDatabase admin -u root -p

db.createUser({
    user: "roberto",
    pwd: "admin",
    roles: [ "readWrite", "dbAdmin" ]
})
```

## Codebeat
[![codebeat badge](https://codebeat.co/badges/9b2dc661-1641-4ad2-97dd-39b40d9484d9)](https://codebeat.co/projects/github-com-rcalumno-visita-core-master)

## travis CI
[![Build Status](https://travis-ci.org/rcalumno/visita-core.svg?branch=master)](https://travis-ci.org/rcalumno/visita-core)

## Codacy Badge
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/aeff89f47acb40fb80eea98598c95fe7)](https://www.codacy.com/app/maniac787/visita-core?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=rcalumno/visita-core&amp;utm_campaign=Badge_Grade)


[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/aeff89f47acb40fb80eea98598c95fe7)](https://www.codacy.com/app/maniac787/visita-core?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=rcalumno/visita-core&amp;utm_campaign=Badge_Coverage)

## snyk
[![Known Vulnerabilities](https://snyk.io/test/github/rcalumno/visita-core/badge.svg?targetFile=requirements.txt)](https://snyk.io/test/github/rcalumno/visita-core?targetFile=requirements.txt)