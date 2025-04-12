function bang \
    -d "Bang arguments up and down to show off your fish skills." \
    -V COLUMNS -V "LINES"
    argparse h/help -- $argv
    if set -q _flag_help;
	echo $COLUMNS 'x' $LINES
    else if set -q _flag_;
    else;
	return 1
    end
end
