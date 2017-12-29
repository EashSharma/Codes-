#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>
#include <string.h>
/*
resistor =1
capacitor = 2
inductor = 3
voltagesource =4
currentsource =5
*/

void printcomponent(int x,int y,characterstics *c)
{
f=fopen("component.svg","a");
int num=c->type;
switch(num)
{FILE *f;
case 1:
	fprintf(f,"<use xlink:href=\"#layer1\" transform=\"translate(%d,%d)\"/>\n",x,y);
	fprintf(f,"<text x=\"%d\" y=\"%d\" font-size=\"15px\" fill=\"black\"/>%s  %f%s</text>\n",x,y-7,c->R->name,c->R->val,c->R->units);
	break;
case 2:
	fprintf(f,"<use xlink:href=\"#layer2\" transform=\"translate(%d,%d)\"/>\n",x,y);
	fprintf(f,"<text x=\"%d\" y=\"%d\" font-size=\"15px\" fill=\"black\"/>%s  %f%s</text>\n",x,y-7,c->C->name,c->C->val,c->C->units);
	break;
case 3:
	fprintf(f,"<use xlink:href=\"#layer3\" transform=\"translate(%d,%d)\"/>\n",x,y);
	fprintf(f,"<text x=\"%d\" y=\"%d\" font-size=\"15px\" fill=\"black\"/>%s  %f%s</text>\n",x,y-7,c->I->name,c->I->val,c->I->units);
	break;
case 4:
	fprintf(f,"<use xlink:href=\"#layer4\" transform=\"translate(%d,%d)\"/>\n",x,y);
	fprintf(f,"<text x=\"%d\" y=\"%d\" font-size=\"15px\" fill=\"black\"/>%s  SINE(%f %f %f%s %f%s %f)</text>\n",x,y-7,c->VS->name,c->VS->dcOffset,c->VS->amplitude,c->VS->frequency,c->VS->freq_units,c->VS->delay,c->VS->delay_units,c->VS->dampingfactor);
	break;
case 5:
	fprintf(f,"<use xlink:href=\"#layer5\" transform=\"translate(x%d,%d)\"/>\n",x,y);
	fprintf(f,"<text x=\"%d\" y=\"%d\" font-size=\"15px\" fill=\"black\"/>%s  SINE(%f %f %f%s %f%s %f)</text>\n",x,y-7,c->IS->name,c->IS->dcOffset,c->IS->amplitude,c->IS->frequency,c->IS->freq_units,c->IS->delay,c->IS->delay_units,c->IS->dampingfactor);
	break;
}
fclose(f);
}
void printline(int x1,int y1,int x2,int y2)
{FILE *f;
f=fopen("loda.txt","a");
fprintf(f,"<line x1=\"%d\" y1=\"%d\" x2=\"%d\" y2=\"%d\"stroke-width=\"2\" stroke=\"black\" />",x1,y1,x2,y2);
fclose(f);
}
void printsvg()
{FILE *f;
f=fopen("loda.svg","a");
fprintf(f,"</svg>\n");
fclose(f);}
int main(void)
{
char *s;
s=(char*)malloc(100*sizeof(char));
scanf("%s",s);
printcomponent(50,50,1,s);
printsvg();
return 0;
}
