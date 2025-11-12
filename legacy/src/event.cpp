#include "event.h"
#include <iostream>
#include "sequence.h"
#include "eventList.h"

const string event::weekdaystr[] = {"Sun","Mon","Tue","Wed","Thu","Fri","Sat"};
const char event::weekdayc[] = {'N','M','T','W','R','F','S'};

event::~event()
{
  //cout << m_desc << endl;
  //cout << m_children.size() << endl;
  //for (vseqi i = m_children.begin(); i != m_children.end(); i++) {
  //  cout<<*i<<endl;}//delete *i;}
  //for (vseqi i = m_children.begin(); i != m_children.end(); i++) {
  //  cout<<*i<<endl;delete *i;}
  while (m_children.begin() != m_children.end()) delete *(m_children.begin());
  while (m_lists.begin() != m_lists.end())
    (*(m_lists.begin()))->removeEvent(this);
  //for (vlisti i = m_lists.begin(); i != m_lists.end(); i++)
  //  (*i)->removeEvent(this);
  //cout << this << " deleted" << endl;
  return;
}

string event::ymdhms() const
{
  // need to resolve seconds...
  //will do so by creating a new tp at seconds res and subtracting.
  time_t y = system_clock::to_time_t(getSgmtEpoch());
  struct tm t = *localtime(&y);
  mstp ttp =
    time_point_cast<milliseconds>(system_clock::from_time_t(mktime(&t)));
  milliseconds dms = getSgmtEpoch() - ttp;
  if (dms.count() < 0)
  {
    cerr << "negative delta ms" << endl;
    ttp -= milliseconds(1000);
    dms += milliseconds(1000);
    y = system_clock::to_time_t(ttp);
  }
  t = *gmtime(&y);

  // 12/45/7890 23:56:89.123/0
  // 123456789012345678901234
  char z[24];
  sprintf(z,"%04d-%02d-%02d %02d:%02d:%02d.%03d",
    t.tm_year+1900,t.tm_mon+1,t.tm_mday,t.tm_hour,t.tm_min,t.tm_sec,
    (short)(dms.count()));

  return z;
}

string event::deltanow() const
{
  milliseconds dms =
    time_point_cast<milliseconds>(system_clock::now()) - getGmtEpoch();

  char neg[] = "+";
  if (dms.count() < 0)
  {
    neg[0] = '-';
    dms *= -1;
  }

  short d = (duration_cast<days>(dms)).count();
  char h = (duration_cast<hours>(dms % days(1))).count();
  char m = (duration_cast<minutes>(dms % hours(1))).count();
  char s = (duration_cast<seconds>(dms % minutes(1))).count();
  short ms = (duration_cast<milliseconds>(dms % seconds(1))).count();

  // -234:67:90:23.567/0
  // 123456789012345678
  char x[18];
  sprintf(x,"%s%03d:%02d:%02d:%02d.%03d",neg,d,h,m,s,ms);

  return x;
}

string event::getFqDesc(bool omitanchor) const
{
  event* q = getAnchor();
  sequence* s = (m_children.empty())?NULL:*(m_children.begin());

  return ((q)? q->getFqDesc(true) : "") + m_desc
    + ((s)? "[" + s->getSeqName() + "]:"
    + ((omitanchor)? "" : s->getAnchorDesc()):"");
}

/*
string event::getShortDesc() const
{
  string anchordesc("");
  event* q = getAnchor();
  string seqName = (q)? ((sequence*)this)->getAnchorDesc() + ":" : "";
  while (q)
  {
    anchordesc = q->getDesc() + ":";
    q = q->getAnchor();
  }
  return anchordesc + ((q)? seqName : m_desc);
}
*/

void event::addChild(sequence* x)
{
  m_children.push_back(x);
  for (vlisti i = m_lists.begin(); i != m_lists.end(); i++) (*i)->addEvent(x);
  return;
}

void event::removeChild(sequence* x)
{
  for (vseqi i = m_children.begin(); i != m_children.end(); i++)
    if (*i==x)
    {
      m_children.erase(i);
      break;
    }
  return;
}

void event::addList(eventList* x)
{
  m_lists.push_back(x);
  //x->addList(this);
  for (vseqi i = m_children.begin(); i != m_children.end(); i++)
    x->addEvent(*i);
  return;
}

void event::removeList(eventList* x)
{
  for (vlisti i = m_lists.begin(); i != m_lists.end(); i++)
    if (*i==x)
    {
      m_lists.erase(i);
      break;
    }
  for (vseqi i = m_children.begin(); i != m_children.end(); i++)
    x->removeEvent(*i);
  return;
}
