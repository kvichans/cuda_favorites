''' Plugin for CudaText editor
Authors:
    Andrey Kvichansky    (kvichans on github.com)
Version:
    '1.0.4 2016-06-22'
ToDo: (see end of file)
'''

import  re, os, json, collections
import  cudatext            as app
from    cudatext        import ed
from    cudax_lib       import log
from    .cd_plug_lib    import *

OrdDict = collections.OrderedDict

FROM_API_VERSION= '1.0.146'

# I18N
_       = get_translation(__file__)

pass;                           # Logging
pass;                          #from pprint import pformat
pass;                          #pfrm15=lambda d:pformat(d,width=15)
pass;                           LOG = (-2==-2)  # Do or dont logging.
pass;                           ##!! waits correction

GAP     = 5

fav_json= app.app_path(app.APP_DIR_SETTINGS)+os.sep+'cuda_favorites.json'
def get_fav_data():
    return json.loads(open(fav_json).read(), object_pairs_hook=OrdDict) \
            if os.path.exists(fav_json) else \
           OrdDict()
def save_fav_data(fvdata):
    open(fav_json, 'w').write(json.dumps(fvdata, indent=4))

def import_SynFav(fn_ini, files):
    # Import from Syn
    chnd    = False
    syn_lns = open(fn_ini, encoding='utf-16').read().splitlines()
    for syn_ln in syn_lns:
        if not os.path.isfile(syn_ln) \
        or any([os.path.samefile(syn_ln, f) for f in files]): continue
        files  += [syn_ln]
        chnd    = True
    return chnd

class Command:
    def add_cur_proj(self):
        pass
    def add_cur_file(self):
        self._add_filename(ed.get_filename())
    def _add_filename(self, fn):
        if not fn:  return
        fvdata  = get_fav_data()
        files   = fvdata.get('fv_files', [])
        if any([os.path.samefile(fn, f) for f in files]):   return
        files  += [fn]
        fvdata['fv_files'] = files
        save_fav_data(fvdata)
        app.msg_status(_('Added to Favorites: ')+fn)
       #def _add_filename
    
    def dlg(self):
#       if app.app_api_version()<'1.0.146':  return app.msg_status(_("Need update CudaText"))   # dlg_custom: "type=tabs"
        pass;                  #LOG and log('=',())
        fvdata  = get_fav_data()
        files   = fvdata.get('fv_files', [])
        fold    = fvdata.get('fv_fold', True)
        last    = fvdata.get('fv_last', 0)
        fvrs_h  = _('Choose file.'
                    '\rUse Alt+1, Alt+2, ..., Alt+9, Alt+0'
                    '\rto direct open file'
                    '\r"1: *", "2: *",..., "9: *", "0: *"')
        brow_h  = _('Choose file to append')#.\rTip: Select "SynFav.ini" for import Favorites from SynWrite.'
        def n2c(n):
            if  1<=n<= 9:                   return str(n)
            if     n==10:                   return '0'
            if 11<=n<=11+ord('Z')-ord('A'): return chr(n-11+ord('A'))
            return ' '
        while True:
            hasf= bool(files)
            itms= [f('{}: {}{}'
                    , n2c(1+nf)
                    , os.path.basename(fn)
                    , ' ('+os.path.dirname(fn)+')' if fold else ''
                    ) 
                    for nf,fn in enumerate(files)]
            itms= itms if itms else [' ']
            btn,vals,chds   = dlg_wrapper(_('Favorites'), GAP+500+GAP,GAP+300+GAP,
                 [dict(           tp='lb'   ,t=GAP          ,l=GAP          ,w=400      ,cap=_('&Files:')   ,hint=fvrs_h        ) # &f
#                ,dict(cid='tabs',tp='tabs' ,t=1,h=25       ,l=50           ,w=300      ,items=['Files', 'Projects']            ) # 
                 ,dict(cid='fvrs',tp='lbx'  ,t=GAP+20,h=250 ,l=GAP          ,w=400-GAP  ,items=itms                     ,en=hasf) # 
                 ,dict(cid='open',tp='bt'   ,t=GAP+20       ,l=GAP+400      ,w=100      ,cap=_('&Open')     ,props='1'  ,en=hasf) #     default
                 ,dict(cid='addc',tp='bt'   ,t=GAP+75       ,l=GAP+400      ,w=100      ,cap=_('&Add opened')                   ) # &a
                 ,dict(cid='brow',tp='bt'   ,t=GAP+100      ,l=GAP+400      ,w=100      ,cap=_('Add&...')   ,hint=brow_h        ) # &.
                 ,dict(cid='delt',tp='bt'   ,t=GAP+135      ,l=GAP+400      ,w=100      ,cap=_('&Delete')               ,en=hasf) # &d
                 ,dict(cid='fvup',tp='bt'   ,t=GAP+210      ,l=GAP+400      ,w=100      ,cap=_('Move &up')              ,en=hasf) # &u
                 ,dict(cid='fvdn',tp='bt'   ,t=GAP+235      ,l=GAP+400      ,w=100      ,cap=_('Move do&wn')            ,en=hasf) # &w
                 ,dict(cid='fold',tp='ch'   ,tid='-'        ,l=GAP          ,w=100      ,cap=_('Show &paths')   ,act='1'        ) # &p
                 ,dict(cid='-'   ,tp='bt'   ,t=GAP+300-28   ,l=GAP+500-100  ,w=100      ,cap=_('Close')                         )
                 ,dict(cid='act0',tp='bt'   ,t=0            ,l=0            ,w=0        ,cap=_('&1')                            ) # &1
                 ,dict(cid='act1',tp='bt'   ,t=0            ,l=0            ,w=0        ,cap=_('&2')                            ) # &2
                 ,dict(cid='act2',tp='bt'   ,t=0            ,l=0            ,w=0        ,cap=_('&3')                            ) # &3
                 ,dict(cid='act3',tp='bt'   ,t=0            ,l=0            ,w=0        ,cap=_('&4')                            ) # &4
                 ,dict(cid='act4',tp='bt'   ,t=0            ,l=0            ,w=0        ,cap=_('&5')                            ) # &5
                 ,dict(cid='act5',tp='bt'   ,t=0            ,l=0            ,w=0        ,cap=_('&6')                            ) # &6
                 ,dict(cid='act6',tp='bt'   ,t=0            ,l=0            ,w=0        ,cap=_('&7')                            ) # &7
                 ,dict(cid='act7',tp='bt'   ,t=0            ,l=0            ,w=0        ,cap=_('&8')                            ) # &8
                 ,dict(cid='act8',tp='bt'   ,t=0            ,l=0            ,w=0        ,cap=_('&9')                            ) # &9
                 ,dict(cid='act9',tp='bt'   ,t=0            ,l=0            ,w=0        ,cap=_('&0')                            ) # &0
                 ],    dict(fvrs=last
#                          ,tabs=0
                           ,fold=fold), focus_cid='fvrs')
            if btn is None or btn=='-': return None
            
            fold    = vals['fold']
            last    = vals['fvrs']
            if btn=='open' and files and last>=0 and os.path.isfile(files[last]):
                app.file_open(files[last])
                break#while
            if btn[0:3]=='act' and files:
                nf  = int(btn[3])
                if nf<len(files) and os.path.isfile(files[nf]):
                    fvdata['fv_last' ] = nf 
                    save_fav_data(fvdata)
                    app.file_open(files[nf])
                    break#while
            
            # Modify
            store_b = 'fold' in chds
            if False:pass
            elif btn=='addc' and ed.get_filename():
                fn      = ed.get_filename()
                if not any([os.path.samefile(fn, f) for f in files]):
                    files  += [fn]
                    store_b = True
            elif btn=='brow':
                fn      = app.dlg_file(True, '', '', '')
                if fn and os.path.basename(fn).upper()=='SynFav.ini'.upper():
                    store_b = import_SynFav(fn, files)
                elif fn and fn not in files:
                    files  += [fn]
                    store_b = True
            elif btn=='delt' and files and last>=0:
                del files[last]
                last    = min(max(0, last), len(files)-1)
                store_b = True
            elif btn in ('fvup', 'fvdn') and files:
                newp    = last + (-1 if btn=='fvup' else +1)
                if 0<=newp<len(files):
                    files[last], files[newp] = files[newp], files[last]
                    last    = newp
                    store_b = True
            
            # Store
            if store_b:
                fvdata['fv_files'] = files
                fvdata['fv_fold' ] = fold 
                fvdata['fv_last' ] = last 
                save_fav_data(fvdata)
           #while
       #def dlg
   #class Command

'''
ToDo
[+][at-kv][20jun16] Moved from cuda_ext
'''
