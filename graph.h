#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
typedef struct Res{
char* name;
double val;
char *units;
char* a;
char* b;
} Resistor;
typedef struct Capacitor{
char *name;
double val;
char *units;
char* a;
char* b;
} Capacitor;
typedef struct Inductor{
char *name;
double val;
char *units;
char* a;
char* b;
} Inductor;
typedef struct VoltageSource{
char *name;
double dcOffset;
double amplitude;
double frequency;
char* freq_units;
double delay;
char* delay_units;
double dampingfactor;
char* a;
char* b;
} VoltageSource;
typedef struct CurrentSource{
char *name;
double dcOffset;
double amplitude;
double frequency;
char* freq_units;
double delay;
char* delay_units;
double dampingfactor;
char* a;
char* b;
} CurrentSource;

struct node 
{
  char* nodename;
  int strnum; 
  struct node *next;
};
struct HASHMAP
{
	struct node *hashtable[10000];	
    char* inversemap[10000];  

}; 

long key(char *str)
{
  char *temp;
  temp=str;
  int i;
  long key1=0;
  for(i=0;i<strlen(temp);i++)
  {
    key1=(key1*256)+*temp;
    key1=key1%10000;
    temp++;
  }
  return key1;
}

void insert(char *str,int num,struct HASHMAP *H)
{
  long key1 =key(str);
  struct node *temp;
  temp=(struct node*)malloc(sizeof(struct node));
  temp->nodename=str;
  temp->strnum=num;
  if(H->hashtable[key1]==NULL)
  {
    H->hashtable[key1]=temp;
    temp->next=NULL;
  }
  else//
  {
    struct node *temp1;
    temp1=H->hashtable[key1];
    while(temp1->next!=NULL)
    temp1=temp1->next;
    
    temp1->next=temp;
    temp1=temp;
    temp1->next=NULL;
  }
   //  ptr[num]=(char *)malloc(100);
       (H->inversemap)[num]=strdup(str);
     //H->inversemap=ptr;//strdup(str);
}
int hashmap(char *str,struct HASHMAP *H)
{
  long key1=key(str);
  struct node *temp=H->hashtable[key1];
  while(temp!=NULL)
  {
  	if(strcmp(temp->nodename,str)==0)
  	{
  		return temp->strnum;
  	}
  	temp=temp->next;
  }
  
  return -1;
}
bool find(char *str,struct HASHMAP *H)
{
	if(hashmap(str,H)==-1)
	return false;
	else
	return true;
}
void update(char *str,int num,struct HASHMAP *H)
{
	long key1=key(str);
	struct node *temp=H->hashtable[key1];
	while(temp!=NULL)
	{
		if(strcmp(temp->nodename,str)==0)
  		{
               // free(H->inversemap[temp->strnum]);
  			temp->strnum=num;
  			break;
  		}
  		temp=temp->next;
	}
}
struct AdjList{
int val;
struct AdjList * next;
};
struct AdjList* addElement(struct AdjList *head,int val){
struct AdjList *temp;
temp=(struct AdjList *)malloc(sizeof(struct AdjList));
temp->val=val;
temp->next=head;
return temp ;
}
typedef struct Characterstics{
int type;
Resistor *R;
Inductor *I;
Capacitor *C;
VoltageSource *VS;
CurrentSource *IS;
}Characterstics;
struct Graph{
struct AdjList ** G;
int *ES;
int *EP;
Characterstics **EC;
struct HASHMAP *H;
int V;
int E;
};
struct Graph * CreateGraph(){
struct Graph * graph;
graph=(struct Graph *)malloc(sizeof(struct Graph));
graph->G=(struct AdjList **)malloc(sizeof( struct AdjList *)*10000);
struct HASHMAP map;
(graph->V)=0;
graph->E=0;

graph->ES=(int *)malloc(40000);
graph->EP=(int *)malloc(40000);
graph->EC=(Characterstics **)malloc(10000*sizeof(Characterstics *));
graph->H=(struct HASHMAP *)malloc(sizeof(struct HASHMAP));
return graph;
}
void addEdge(struct Graph *graph,char *src,char *dest,Characterstics *C){

int a,b;
if(find(src,graph->H)==false){
a=graph->V+1;
graph->V++;
insert(src,a,graph->H);

}else a=hashmap(src,graph->H);
if(find(dest,graph->H)==false){
b=graph->V+1;
graph->V++;
insert(dest,b,graph->H);
}else b=hashmap(dest,graph->H);
int e=graph->E+1;
graph->E++;
(graph->ES)[e]=a;
(graph->EP)[e]=b;
(graph->EC)[e]=C;
struct AdjList *temp;
temp =(graph->G)[a];
(graph->G)[a]=addElement(temp,e);
// look upon this
(graph->G)[b]=addElement((graph->G)[b],e);
//look upon this

}
