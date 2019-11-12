# QGIS Tile Builder

Formålet med projektet er at have en automatisk pipeline for generering af .mbtiles-filer fra QGIS-projekter.

## Overblik over arkitektur

### Crontab

Der køres en crontab i en dockercontainer, der er ansvarlig for at styre hvornår de forskellige projekter bygges. Crontabben ændres ved at redigere files `cron` i roden af projektet.
I denne fil kaldes `python3 /opt/src/run.py` med en række parametre, der styrer hvordan projektet bygges.

Kaldene følger denne form

```sh
python3 /opt/src/run.py --project /path/to/project.qgz --minzoom 12 --maxzoom 20 --extend "bbox-coords"
```

### SFTP

Der ligger en SFTP server i løsningen, der gør det nemt at opdatere QGIS-projekterne. Offentlignøglerne til SFTP-serveren ligger i mappen `pub_keys`.
Serveren er eksponeret på port 2222, og brugeren skal forbinde til brugeren `gis` for at uploade projekter.

## Tilføjelse af et nyt projekt

Først uploades projektet over SFTP. Det gøres ved at forbinde til SFTP-serveren med en FTP klient, f.eks WinSCP på windows.
Her placeres projektet i mappen `projekter`.

Dernæst skal der tilføjes en post i crontabben. Dette gøres ved at redigere i cron-files i projektroden. Du kan med fordel kopiere en af de eksisterende linjer, da det oftest kun er projekt-stien, der skal redigeres.
Mappen `projekter` fra FTP vil i containeren blive mounted til /opt/projekter/.

Cron filen kan med fordel redigeres på github og pulles til serveren. På den måde, har vi en backup af crontabben, og undgår mergekonflikter ved opdateringer.

## Opdatering af eksisterende projekt

0. Hvis du ikke har en kopi af projektet, kan du hente det fra serveren over FTP
1. Lav dine ændringer
1. Upload den nye version over FTP. Overskriv den gamle version.
1. Profit

Hvis du ikke har behov for at ændre på opdateringsfrekvensen af projektet, kan du ignorere cron, og blot opdatere over FTP.
