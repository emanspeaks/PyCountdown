#include "eventList.h"
#include <iostream>
#include <iomanip>
#include <fstream>
#include <map>
#include "event.h"
#include "epoch.h"
#include "sequence.h"

bool compareEvents::operator()(event* t1, event* t2) //true if t1 high priority
{
   if (*t2 > *t1) return true;
   else if (*t1 == *t2 && t2->getDesc() > t1->getDesc()) return true;
   else return false;
}

string eventList::trim(string s)
{
  size_t i = s.find_first_not_of(" \t");
  return (i!=string::npos)? s.substr(i):"";
}

string eventList::tokenize(string tokens, const string &s, size_t &a, size_t &z)
{
  string x("");
  z = s.find_first_of("\\"+tokens,a);
  while (z != string::npos && s[z] == '\\')
  {
    x += s.substr(a,z-a);
    if (++z < s.length()) x += s[z];
    a = ++z;
    z = s.find_first_of("\\"+tokens,a);
  }
  x = trim(x + s.substr(a,z-a));
  a = z+1;
  return x;
}

int eventList::getLongestFqDesc() const
{
  int n, nmax = 1;
  for (eseti i = m_collection.begin(); i != m_collection.end(); i++)
  {
    n = (*i)->getFqDesc().length();
    nmax = (n>nmax)? n : nmax;
  }
  return nmax;
}

/*
int eventList::getLongestShortDesc() const
{
  int n, nmax = 1;
  for (eseti i = m_collection.begin(); i != m_collection.end(); i++)
  {
    n = (*i)->getShortDesc().length();
    nmax = (n>nmax)? n : nmax;
  }
  return nmax;
}
*/

eventList::eventList(string fn)
{
  ifstream f(fn);
  string buf;
  if (f.is_open())
  {
    string line;
    while (!f.eof())
    {
      getline(f,line);
      buf += line;
    }
    f.close();
  }
  else throw string("Unable to open file");

  fromSerialized(buf);
  return;
}

void eventList::addEvent(event* x)
{
  m_collection.insert(x);
  x->addList(this);
  return;
}

void eventList::removeEvent(event* x)
{
  m_collection.erase(x);
  x->removeList(this);
  return;
}

void eventList::printList() const
{
  int nmax = getLongestFqDesc();
  for (eseti i = m_collection.begin(); i != m_collection.end(); i++)
    cout<<setw(nmax)<<(*i)->getFqDesc()<<" EPOCH:"<<(*i)->ymdhms()<<endl;
  return;
}



void eventList::printListCountdown() const
{
  int nmax = getLongestFqDesc();
  for (eseti i = m_collection.begin(); i != m_collection.end(); i++)
    cout << setw(nmax) << (*i)->getFqDesc() << ":" << (*i)->deltanow() << endl;
  return;
}

void eventList::fromSerialized(string s)
{
  map<string,epoch*> seqlist;

  size_t a = 0, z;
  string line(""), key(""), seq(""), st3("");
  short t1, t2;
  epoch* q;
  do
  {
    line = tokenize("@[=}",s,a,z);
    if (z<s.length())
      switch (s[z])
      {
        case '[':
          key = tokenize("]",s,a,z);
          line = tokenize("=",s,a,z);
        case '=':
          t1 = stoi(tokenize(":",s,a,z));
          t2 = stoi(tokenize(":",s,a,z));
          st3 = tokenize(":;",s,a,z);
          if (z<s.length() && s[z] == ';')
          {
            milliseconds offset = hours(t1);
            offset += (t1<0?-1:1)*minutes(t2);
            offset += (t1<0?-1:1)*milliseconds((short)(1000*stof(st3)));

            sequence* p =
            new sequence(line,seqlist[seq],offset,seq,seqlist[seq]->getDesc());
            cout << p << ":" << line << endl;

            if (key.length())
            {
              q = new epoch(*(seqlist[key]));
              q->setAnchor(p);
              delete q;
            }
          }
          else
          {
            short t3 = stoi(st3);
            short t4 = stoi(tokenize(":",s,a,z));
            string st5 = tokenize(":;",s,a,z);
            short t5 = 0;
            short t6 = 0;
            bool ymd = false;
            short t7 = 0;
            if (z<s.length() && s[z] == ';') t5 = 1000*stof(st5);
            else
            {
              t5 = stoi(st5);
              if (a<s.length() && (s[a] == '+' || s[a] == '-'))
                t6 = stoi(tokenize(";",s,a,z));
              else
              {
                ymd = true;
                t6 = 1000*stof(tokenize(":;",s,a,z));
                if (z<s.length() && s[z] == ':') t7 = stoi(tokenize(";",s,a,z));
              }
            }

            if (key.length())
            {
              q = new epoch(*(seqlist[key]));
              q->setDesc(line);
              if (ymd) q->setEpoch(t1, t2, t3, t4, t5, t6/1000.0F, t7);
              else q->setEpoch(t1, t2, t3, t4, t5/1000.0F, t6);
            }
            else if (ymd)
              q = new epoch(line, t1, t2, t3, t4, t5, t6/1000.0F, t7);
            else q = new epoch(line, t1, t2, t3, t4, t5/1000.0F, t6);

            addEvent(q);
          }

          key = "";
          break;

        case '@':
          seq = line;
          line = tokenize("{",s,a,z);
          q = new epoch();
          q->setDesc(line);
          seqlist[seq] = q;
          cout << q << ":" << line << endl;
          break;

        case '}':
          seq = "";
          break;
      }
  }
  while (a < s.length());

  for (map<string,epoch*>::iterator i = seqlist.begin();
    i != seqlist.end(); i++)
    delete i->second;

  return;

  /*
    string seqname = tokenize("@",s,a,z);
    lastseq = seqname;

    string anchordesc = tokenize("{",s,a,z);

    string e("");
    a = z + 2;
    z = s.find_first_of("}",a);
    while (z != string::npos && s[z-1] == '\\')
    {
      e += s.substr(a,++z-a);
      a = ++z;
      z = s.find_first_of("}",a);
    }
    e += s.substr(a,z-a);

    //parse events
    vector<sequence*> elist;
    size_t b = 0, y;
    do
    {
      string key(""), desc = tokenize("[=",e,b,y);
      if (--y < e.length() && e[y] == '[')
      {
        key = tokenize("]",e,b,y);
        desc = tokenize("=",e,b,y);
      }

      milliseconds offset = hours(stoi(tokenize(":",e,b,y)));
      offset +=
        (offset<milliseconds(0)?-1:1)*minutes(stoi(tokenize(":",e,b,y)));
      offset +=
        (offset<milliseconds(0)?-1:1)
        * milliseconds((short)(1000*stof(tokenize(";",e,b,y))));

      sequence* q = new sequence(desc,NULL,offset,seqname,anchordesc);
      if (key.length())
        for (vseqi i = seqlist[key].begin(); i != seqlist[key].end(); i++)
          q->addChild(new sequence(**i));
      elist.push_back(q);
    }
    while (b < e.length());

    seqlist[seqname] = elist;

    a = ++z;
  }
  while (a < s.length());

  for (vseqi i = seqlist[lastseq].begin(); i != seqlist[lastseq].end(); i++)
    (new sequence(**i))->setAnchor(anchor);

  for (vseqi i = seqlist[lastseq].begin(); i != seqlist[lastseq].end(); i++)
    delete *i;

  return;
  */
}

// I KNOW THIS DOESN'T WORK YET AND I DON'T REALLY CARE
/*
string sequence::serialize() const
{
  string buf = m_seqname + "@";
  buf += m_anchordesc + "{";
  for (vseqi i = m_children.begin(); i != m_children.end(); i++)
  {
    buf += (*i)->getDesc() + "=";
    milliseconds offset = (*i)->getOffset();
    if (offset < milliseconds(0))
    {
      buf += "-";
      offset *= -1;
    }
    buf += to_string((duration_cast<hours>(offset)).count()) + ":";
    buf += to_string((duration_cast<minutes>(offset % hours(1))).count())+":";
    buf += to_string((duration_cast<milliseconds>(offset % minutes(1))).count()
      /1000.0) + ";";
  }
  buf += "}";

  return buf;
}
*/

