# Define an inline function to strip URL parameters
stripParams() {
  local urls=("$@")
  local stripped_urls=""
  for url in "${urls[@]}"; do
    # Remove everything from the '?' character onward using parameter expansion
    stripped_urls+="${url%%\?*} "
  done
  echo "$stripped_urls"
}

# \ ]* # use this RegEx to remove the query tags
# ./start.sh SPOTIFY LINKS HERE
export SONGS=$(stripParams $@)

python -m spotdl download $SONGS --sponsor-block --bitrate disable --headless --user-auth --preload