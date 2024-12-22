
#!/bin/sh
echo "# "${1}
echo "Q,A,R,F"

sed  '/^$/d' ${1} | sed 's/,//g' | awk '$0!~/\(/{print $0, " ( )"} $0~/\(/{print $0}' | sed 's/ (/\, (/g' | awk 'BEIGN{RS=","} $1!~/\#/{print $0, ", 0, 0"}'  | sed 's/(//g' | sed 's/)//g' | sed 's/\t/ /g' | sed 's/ \{2,\}/ /g' | sed 's/ ,}/,/g' | uniq
 
