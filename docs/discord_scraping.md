## Getting the Discord Data

``` bash
cd /path/to/discord/data
DISCORD_TOKEN="Jibberish"
export_folder="DiscordAccountName"
mkdir $export_folder
cd $export_folder
my_dir="pwd"
docker run --rm -v $(pwd)/$export_folder:/out \
	--name discord02 \
	tyrrrz/discordchatexporter:stable exportall \
	-t $DISCORD_TOKEN \
	--media \
	--dateformat "yyyy-MM-dd H:mm:ss.ffff" \
	-f Json -p 80mb
```