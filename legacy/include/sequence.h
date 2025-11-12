#ifndef SEQUENCE_H
#define SEQUENCE_H

#include <chrono>
#include <string>
#include "event.h"

//using namespace std;
using namespace std::chrono;

class sequence: public event
{
  private:
    event* m_anchor;
    milliseconds m_offset;
    string m_seqname;
    string m_anchordesc;

  public:
    sequence():
      m_anchor(NULL),
      m_offset(milliseconds(0)),
      m_seqname(""),
      m_anchordesc("")
      {}
    sequence(string desc, event* anchor, milliseconds offset,
      string seqname, string anchordesc):
      event(desc),
      m_anchor(NULL),
      m_offset(offset),
      m_seqname(seqname),
      m_anchordesc(anchordesc)
      {setAnchor(anchor); return;}
    //sequence(event* anchor, ifstream& f);
    sequence(const sequence& x);
    ~sequence();

    sequence& operator=(sequence rhs);

    void setAnchor(event* anchor);
    event* getAnchor() const {return m_anchor;}
    void getOffset(milliseconds x) {m_offset = x; return;}
    milliseconds getOffset() const {return m_offset;}

    void setSeqName(string desc) {m_seqname = desc; return;}
    string getSeqName() const {return m_seqname;}
    void setAnchorDesc(string desc) {m_anchordesc = desc; return;}
    string getAnchorDesc() const {return m_anchordesc;}

    mstp getGmtEpoch() const {return m_anchor->getGmtEpoch()+m_offset;}
    mstp getSgmtEpoch() const {return m_anchor->getSgmtEpoch()+m_offset;}
};

#endif // SEQUENCE_H
