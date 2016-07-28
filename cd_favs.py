''' Plugin for CudaText editor
Authors:
    Andrey Kvichansky    (kvichans on github.com)
Version:
    '1.0.8 2016-07-28'
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

#GAP     = 5

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
        try:
            import cuda_project_man
        except ImportError:
            app.msg_status(_('Project Manager plugin not installed'))
            return
        
        pjm_info= cuda_project_man.global_project_info
        fn      = pjm_info.get('filename', '')
        if fn:
            self._add_filename(fn, True)
        else:
            app.msg_status(_('Project Manager plugin has not opened project'))

    def add_cur_file(self):
        self._add_filename(ed.get_filename())
        
    def _add_filename(self, fn, is_project=False):
        if not fn:  return
        s_key = 'fv_projs' if is_project else 'fv_files'
        fvdata  = get_fav_data()
        files   = fvdata.get(s_key, [])
        if any([os.path.samefile(fn, f) for f in files]):
            return app.msg_status(_('Already in Favorites: ')+fn)
        files  += [fn]
        fvdata[s_key] = files
        save_fav_data(fvdata)
        app.msg_status(_('Added to Favorites: ')+fn)
       #def _add_filename
    
    def dlg(self):
        if app.app_api_version()<'1.0.146':  return app.msg_status(_("Need update CudaText"))   # dlg_custom: "type=tabs"
        pass;                  #LOG and log('=',())
        fvdata  = get_fav_data()
        tab_nms = fvdata.get('fv_tabs', [_('Fi&les'), _('Pro&jects')])
        tabs    = fvdata.get('fv_tab', 0)
        files   = fvdata.get('fv_files', [])
        projs   = fvdata.get('fv_projs', [])
        fold    = fvdata.get('fv_fold', True)
        last    = fvdata.get('fv_last', 0)
        fvrs_h  = _('Choose file to open.')
        brow_h  = _('Choose file to append.')
        def n2c(n):
            if  1<=n<=10:                   return str(n%10)
            if 11<=n<=11+ord('Z')-ord('A'): return chr(n-11+ord('A'))
            return ' '
        while True:
            paths   = files if tabs==0 else projs
            last    = min(max(0, last), len(paths)-1)
            hasf    = bool(paths)
            itms    = [f('{}: {}{}'
                    , n2c(1+nf)
                    , os.path.basename(fn)
                    , ' ('+os.path.dirname(fn)+')' if fold else ''
                    ) 
                    for nf,fn in enumerate(paths)]
            itms    = itms if itms else [' ']
            aid,vals,chds   = dlg_wrapper(_('Favorites'), 500+10,300+10,
                 [
#                 dict(           tp='lb'   ,t=5            ,l=5            ,w=400      ,cap=_('&Files:')   ,hint=fvrs_h        ) # &f
                  dict(cid='tabs',tp='tabs' ,t=5,h=30       ,l=5            ,w=400-3    ,items=tab_nms          ,act='1'        ) # 
                 ,dict(cid='fvrs',tp='lbx'  ,t=5+23,h=240   ,l=5            ,w=400-5    ,items=itms                     ,en=hasf)
                 ,dict(cid='open',tp='bt'   ,t=5+20         ,l=5+400        ,w=100      ,cap=_('&Open')     ,props='1'  ,en=hasf) #     default
                 ,dict(cid='addc',tp='bt'   ,t=5+65         ,l=5+400        ,w=100      ,cap=_('&Add opened')           ,en=(tabs==0)) # &a
                 ,dict(cid='brow',tp='bt'   ,t=5+90         ,l=5+400        ,w=100      ,cap=_('Add&...')   ,hint=brow_h        ) # &.
                 ,dict(cid='delt',tp='bt'   ,t=5+135        ,l=5+400        ,w=100      ,cap=_('&Delete')               ,en=hasf) # &d
                 ,dict(cid='fvup',tp='bt'   ,t=5+180        ,l=5+400        ,w=100      ,cap=_('Move &up')              ,en=hasf) # &u
                 ,dict(cid='fvdn',tp='bt'   ,t=5+205        ,l=5+400        ,w=100      ,cap=_('Move do&wn')            ,en=hasf) # &w
                 ,dict(cid='fold',tp='ch'   ,tid='-'        ,l=5            ,w=100      ,cap=_('Show &paths')   ,act='1'        ) # &p
                 ,dict(cid='help',tp='bt'   ,t=5+300-53     ,l=5+500-100    ,w=100      ,cap=_('&Help')                         ) # &h
                 ,dict(cid='-'   ,tp='bt'   ,t=5+300-28     ,l=5+500-100    ,w=100      ,cap=_('Close')                         )
                 ]+
                 [dict(cid='act'+str(n),tp='bt',cap='&'+str((n+1)%10),t=0,l=0,w=0) for n in range(10)]                           # &1 - &0
                 ,    dict(fvrs=last
                           ,tabs=tabs
                           ,fold=fold), focus_cid='fvrs')
            if aid is None or aid=='-': return None
            if aid=='help':
                dlg_wrapper(_('Help for "Favorites"'), 410, 310,
                     [dict(cid='htxt',tp='me'    ,t=5  ,h=300-28,l=5          ,w=400  ,props='1,0,1'  ) #  ro,mono,border
                     ,dict(cid='-'   ,tp='bt'    ,t=5+300-23    ,l=5+400-80   ,w=80   ,cap=_('&Close'))
                     ], dict(htxt=_(  '• Quick opening.'
                                    '\rUse Alt+1, Alt+2, ..., Alt+9, Alt+0'
                                    '\rto direct open file'
                                    '\r"1: *", "2: *",..., "9: *", "0: *"'
                                    '\r '
                                    '\r• Import. '
                                    '\rSelect "SynFav.ini" for "Add..." to import Favorites from SynWrite.'
                                    '\rSee "SynFav.ini" in folder "SynWrite/Settings".'
                                    )
                     ), focus_cid='htxt')
                continue#while
            
            fold    = vals['fold']
            last    = vals['fvrs']
            tabs    = vals['tabs']
            if aid=='open' and paths and last>=0 and os.path.isfile(paths[last]):
                app.file_open(paths[last])
                break#while
            if aid[0:3]=='act' and paths:
                nf  = int(aid[3])
                if nf<len(paths) and os.path.isfile(paths[nf]):
                    fvdata['fv_last' ] = nf 
                    save_fav_data(fvdata)
                    app.file_open(paths[nf])
                    break#while
                    
            if aid=='tabs':
                pass;          #LOG and log('tabs={}',(tabs))
                continue#while
            
            # Modify
            store_b = 'fold' in chds
            if False:pass
            elif aid=='addc':
                fn      = ed.get_filename()
                if fn and not any([os.path.samefile(fn, f) for f in paths]):
                    paths  += [fn]
                    store_b = True
            elif aid=='brow':
                fn      = app.dlg_file(True, '', '', '')
                if fn and os.path.basename(fn).upper()=='SynFav.ini'.upper():
                    store_b = import_SynFav(fn, paths)
                elif fn and not any([os.path.samefile(fn, f) for f in paths]):
                    paths  += [fn]
                    store_b = True
            elif aid=='delt' and paths and last>=0:
                del paths[last]
                last    = min(max(0, last), len(paths)-1)
                store_b = True
            elif aid in ('fvup', 'fvdn') and paths:
                newp    = last + (-1 if aid=='fvup' else +1)
                if 0<=newp<len(paths):
                    paths[last], paths[newp] = paths[newp], paths[last]
                    last    = newp
                    store_b = True
            
            # Store
            if store_b:
                fvdata['fv_tab']    = tabs
                fvdata['fv_files']  = files
                fvdata['fv_projs']  = projs
                fvdata['fv_fold' ]  = fold 
                fvdata['fv_last' ]  = last 
                save_fav_data(fvdata)
           #while
       #def dlg
   #class Command

'''
ToDo
[+][at-kv][20jun16] Moved from cuda_ext
'''
