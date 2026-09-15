"""Bounded reload probes that cover correction consequences, not only output forms."""
import json
import maintenance_task as task


def select(rows, limit=8):
    assert rows and limit>=6
    selected=[];seen=set()
    def add(row):
        key=json.dumps(row['case'],sort_keys=True)
        if key not in seen and len(selected)<limit:
            selected.append(row);seen.add(key)
    def first(predicate):
        for r in rows:
            if predicate(r):add(r);return
    def changed(r):
        return r['version']>0 and task.oracle(r['case'],r['version'])!=task.oracle(r['case'],r['version']-1)
    def stock(r):return r['case']['stock']==1
    # First probes explicitly exercise state-changing revisions and old corrections.
    first(lambda r: changed(r) and stock(r) and r['case']['entity'] in task.ACQUIRED[:2])
    first(lambda r: changed(r) and stock(r) and r['case']['entity'] in task.ACQUIRED[2:])
    first(lambda r: changed(r) and stock(r) and r['case']['entity'] not in task.ACQUIRED+task.TARGETS)
    first(lambda r: r['version']==2 and stock(r) and task.oracle(r['case'],1)!=task.oracle(r['case'],0))
    first(lambda r: r['case']['entity'] not in task.ACQUIRED+task.TARGETS)
    first(lambda r: True)
    signatures=set()
    for r in rows:
        signature=(r['expected'],r['scores']['complete'])
        if signature not in signatures:add(r);signatures.add(signature)
    return selected
