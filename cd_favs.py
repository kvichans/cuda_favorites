''' Plugin for CudaText editor
Authors:
    Andrey Kvichansky    (kvichans on github.com)
Version:
    '1.0.3 2016-06-21'
ToDo: (see end of file)
'''

import  re, os, json
import  cudatext            as app
from    cudatext        import ed
from    cudax_lib       import log
from    .cd_plug_lib    import *
from collections import OrderedDict as OrdDict

# I18N
_       = get_translation(__file__)

pass;                           # Logging
pass;                          #from pprint import pformat
pass;                          #pfrm15=lambda d:pformat(d,width=15)
pass;                           LOG = (-2==-2)  # Do or dont logging.
pass;                           ##!! waits correction

GAP     = 5

fav_json= app.app_path(app.APP_DIR_SETTINGS)+os.sep+'cuda_favorites.json'

def listbox_prefix(n):
    if 0<=n<=8:
        s = str(n+1)
    elif n==9:
        s = '0'
    elif 10<=n<=10+ord('Z')-ord('A'):
        s = chr(n-10+ord('A'))
    else:
        s = ' '
    return s + ': '

class Command:
    def add_filename(self, fn):
        if not fn:  return
        app.msg_status(_('Added to Favorites: ')+fn)
        
        stores  = json.loads(open(fav_json).read(), object_pairs_hook=OrdDict) \
                    if os.path.exists(fav_json) else OrdDict()
        files   = stores.get('fv_files', [])
        if any([os.path.samefile(fn, f) for f in files]):   return
        files  += [fn]
        stores['fv_files'] = files
        open(fav_json, 'w').write(json.dumps(stores, indent=4))
       #def add_filename
       
    def add_cur_file(self):
        self.add_filename(ed.get_filename())
    def add_cur_project(self):
        pass
    
    def dlg(self):
        pass;                  #LOG and log('=',())
        stores  = json.loads(open(fav_json).read(), object_pairs_hook=OrdDict) \
                    if os.path.exists(fav_json) else OrdDict()
        files   = stores.get('fv_files', [])
        fold    = stores.get('fv_fold', True)
        last    = stores.get('fv_last', 0)
        brow_h  = 'Select file to append.\rTip: Select "SynFav.ini" for import Favorites from SynWrite.'
        while True:
            hasf= bool(files)
            itms= [
                    listbox_prefix(n) + 
                    os.path.basename(fv) + 
                    ('  ('+os.path.dirname(fv)+')' if fold else '') 
                    for (n, fv) in enumerate(files)
                    ]
            itms= itms if itms else [' ']
            btn,vals,chds   = dlg_wrapper(_('Favorites'), GAP+500+GAP,GAP+300+GAP,     #NOTE: dlg-favorites
                 [dict(           tp='lb'   ,t=GAP          ,l=GAP          ,w=400      ,cap=_('&Files:')                       ) # &f
                 ,dict(cid='fvrs',tp='lbx'  ,t=GAP+20,h=250 ,l=GAP          ,w=400-GAP  ,items=itms                     ,en=hasf) # 
                 ,dict(cid='open',tp='bt'   ,t=GAP+20       ,l=GAP+400      ,w=100      ,cap=_('&Open')     ,props='1'  ,en=hasf) #     default
                 ,dict(cid='addc',tp='bt'   ,t=GAP+70       ,l=GAP+400      ,w=100      ,cap=_('&Add opened')                   ) # &a
                 ,dict(cid='brow',tp='bt'   ,t=GAP+95      ,l=GAP+400      ,w=100      ,cap=_('Add&...')   ,hint=brow_h        ) # &.
                 ,dict(cid='delt',tp='bt'   ,t=GAP+120      ,l=GAP+400      ,w=100      ,cap=_('&Delete')               ,en=hasf) # &d
                 ,dict(cid='fvup',tp='bt'   ,t=GAP+170      ,l=GAP+400      ,w=100      ,cap=_('Move &up')              ,en=hasf) # &u
                 ,dict(cid='fvdn',tp='bt'   ,t=GAP+195      ,l=GAP+400      ,w=100      ,cap=_('Move do&wn')            ,en=hasf) # &w
                 ,dict(cid='fold',tp='ch'   ,t=GAP+20+250+GAP ,l=GAP        ,w=100      ,cap=_('Show &paths')   ,act='1'        ) # &p
                 ,dict(cid='-'   ,tp='bt'   ,t=GAP+245      ,l=GAP+500-100  ,w=100      ,cap=_('Close')                         )
                 ],    dict(fvrs=last
                           ,fold=fold), focus_cid='fvrs')
            if btn is None or btn=='-': return None
            
            store_b = fold != vals['fold']
            fold    = vals['fold']
            last    = vals['fvrs']
            if btn=='open' and files and last>=0 and os.path.isfile(files[last]):
                app.file_open(files[last])
                break#while
            
            # Modify
#           store_b = False
            if False:pass
            elif btn=='addc' and ed.get_filename():
                fn      = ed.get_filename()
                if not any([os.path.samefile(fn, f) for f in files]):
                    files  += [fn]
                    store_b = True
            elif btn=='brow':
                fl      = app.dlg_file(True, '', '', '')
                if fl and os.path.basename(fl).upper()=='SynFav.ini'.upper():
                    # Import from Syn
                    syn_lns = open(fl, encoding='utf-16').read().splitlines()
                    for syn_ln in syn_lns:
                        if os.path.isfile(syn_ln) and syn_ln not in files:
                            files  += [syn_ln]
                            store_b = True
                elif fl and fl not in files:
                    files  += [fl]
                    store_b = True
            elif btn=='delt' and files and last>=0:
                del files[last]
                last    = max(0, len(files)-1)
                store_b = True
            elif btn in ('fvup', 'fvdn') and files:
                newp    = last + (-1 if btn=='fvup' else +1)
                if 0<=newp<len(files):
                    files[last], files[newp] = files[newp], files[last]
                    last    = newp
                    store_b = True
            
            # Store
            if store_b:
                stores['fv_files'] = files
                stores['fv_fold' ] = fold 
                stores['fv_last' ] = last 
                open(fav_json, 'w').write(json.dumps(stores, indent=4))
           #while
       #def dlg
   #class Command

'''
ToDo
[+][at-kv][20jun16] Moved from cuda_ext
'''
