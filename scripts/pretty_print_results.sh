for f in data/*/*results.csv;
    do echo -ne "\n\n==================$f=================="
    cat $f
done;
