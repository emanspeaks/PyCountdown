#include "sequence.h"

sequence::sequence(const sequence& rhs)
{
  m_anchor = rhs.m_anchor;
  m_desc = rhs.m_desc;
  m_offset = rhs.m_offset;
  m_seqname = rhs.m_seqname;
  m_anchordesc = rhs.m_anchordesc;

  //don't copy m_lists because this will get updated when you setAnchor()
  if (m_anchor) setAnchor(m_anchor);

  vector<sequence*> tmp = rhs.m_children;
  for (vseqi i = tmp.begin(); i != tmp.end(); i++)
      (new sequence(**i))->setAnchor(this);

  return;
}

sequence::~sequence()
{
  if (m_anchor) m_anchor->removeChild(this);
  return;
}

sequence& sequence::operator=(sequence rhs)
{
  swap(m_anchor, rhs.m_anchor);
  swap(m_desc, rhs.m_desc);
  swap(m_offset, rhs.m_offset);
  swap(m_seqname, rhs.m_seqname);
  swap(m_anchordesc, rhs.m_anchordesc);
  swap(m_lists, rhs.m_lists);
  swap(m_children, rhs.m_children);

  return *this;
}

void sequence::setAnchor(event* anchor)
{
  if (m_anchor) m_anchor->removeChild(this);
  m_anchor = anchor;
  if (m_anchor) m_anchor->addChild(this);
  return;
}

