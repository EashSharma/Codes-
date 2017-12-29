#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdbool.h>
#include <string.h>
struct node 
{
  char* nodename;
  int strnum; 
  struct node *next;
};
struct HASHMAP
{
	struct node *hashtable[10000];	
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
  else
  {
    struct node *temp1;
    temp1=H->hashtable[key1];
    while(temp1->next!=NULL)
    temp1=temp1->next;
    
    temp1->next=temp;
    temp1=temp;
    temp1->next=NULL;
  }
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
  			temp->strnum=num;
  			break;
  		}
  		temp=temp->next;
	}
}
int main(void)
{
  struct HASHMAP map;
  char *s,*t;
  s=(char*)malloc(100*sizeof(char));
  t=(char*)malloc(100*sizeof(char));
  scanf("%s %s",s,t);
  insert(s,1,&map);
  printf(" %d ",hashmap(s,&map));
  update(s,2,&map);
  printf(" %d ",hashmap(s,&map));
  if(find(s,&map))
  {
    printf("lund loda");
  }
  if(!find(t,&map))
  {
    printf(" maa chuda li");
  }

  return 0;
}