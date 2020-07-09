''' Plugin for CudaText editor
Authors:
    Andrey Kvichansky    (kvichans on github.com)
Version:
    '1.2.03 2020-07-09'
ToDo: (see end of file)
'''

import  re, os, json, collections
import  cudatext            as app
from    cudatext        import ed
from    cudax_lib       import log
from    .cd_kv_base     import *        # as part of this plugin
from    .cd_kv_dlg      import *        # as part of this plugin

OrdDict = collections.OrderedDict
d       = dcta      # To use keys as attrs: o=dcta(a=b); x=o.a; o.a=x

# I18N
_       = get_translation(__file__)

pass;                           # Logging
pass;                          #from pprint import pformat
pass;                          #pfrm15=lambda d:pformat(d,width=15)
pass;                          #LOG = (-2==-2)  # Do or dont logging.
pass;                           ##!! waits correction

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
    def fav_open_1(self):   self.fav_open(1-1)
    def fav_open_2(self):   self.fav_open(2-1)
    def fav_open_3(self):   self.fav_open(3-1)
    def fav_open_4(self):   self.fav_open(4-1)
    def fav_open_5(self):   self.fav_open(5-1)
    def fav_open_6(self):   self.fav_open(6-1)
    def fav_open_7(self):   self.fav_open(7-1)
    def fav_open_8(self):   self.fav_open(8-1)
    def fav_open_9(self):   self.fav_open(9-1)
    def fav_open(self, pos):
        fvdata  = get_fav_data()
        files   = fvdata.get('fv_files', [])
        if not(0<=pos<len(files)):                  return app.msg_status(f(_('No favorite at #{}'), 1+pos))
        path    = files[pos]
        if os.path.isdir(path):
            path= app.dlg_file(True, '', path, '')
            if not path:                            return
        if not os.path.isfile(path):                return app.msg_status(f(_('Not exist: {}'), path))
        app.file_open(path)
    
    def add_cur_file(self):
        self._add_filename(ed.get_filename())
        
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
            app.msg_status(_('Project Manager has no opened project'))

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
        pass;                  #LOG and log('=',())
        M,m     = type(self),self
        fvdata  = get_fav_data()
        files   = fvdata.get('fv_files', [])
        projs   = fvdata.get('fv_projs', [])
        fold    = fvdata.get('fv_fold', True)
        itab    = fvdata.get('fv_tab', 0)
        flast   = fvdata.get('fv_flast', -1)
        plast   = fvdata.get('fv_plast', -1)
        flast   = min(max(0, flast), len(files)-1) if files else -1
        plast   = min(max(0, plast), len(projs)-1) if projs else -1

        def n2c(n):
            if  1<=n<=10:                   return str(n%10)
            if 11<=n<=11+ord('Z')-ord('A'): return chr(n-11+ord('A'))
            return ' '
        get_its = lambda lst, fo: [f('{}: {}{}'
                                , n2c(1+nf)
                                , os.path.basename(fn) 
                                    if os.path.isfile(fn) else 
                                  '['+os.path.basename(fn)+']' 
                                    if os.path.isdir(fn) else 
                                  '? '+os.path.basename(fn) 
                                , ' ('+os.path.dirname(fn)+')' if fo else ''
                                ) 
                                for nf,fn in enumerate(lst)]
        itfs    = get_its(files, fold)
        itps    = get_its(projs, fold)

        enopen  = itab==0 and itfs and flast>=0 or \
                  itab==1 and itps and plast>=0
        enaddc  = itab==0 and bool(ed.get_filename('*'))

        def do_act(ag, cid, dt=''):
            scam    = ag.scam()
            pass;              #log("scam,cid,val={}",(scam, cid, ag.val(cid)))
            fo      = ag.val('fo')
            its     = ag.val('ts')
            lst     = files if 0==its else projs
            pos     = ag.val('fs'if 0==its else 'ps')
            if cid=='he':
                m.dlg_help()
                return []
            if cid=='ts':
                return d(ctrls=d(fs=d(vis=0==its)
                                ,ps=d(vis=1==its)
                                ,ac=d(en =(0==its and bool(ed.get_filename('*')))) ))
            if cid=='fo':
                return d(ctrls=d(fs=d(items=get_its(files, fo)  ,val=ag.val('fs'))
                                ,ps=d(items=get_its(projs, fo)  ,val=ag.val('ps')) )
                        ,fid='fs' if 0==its else 'ps')
            # Open
            if cid=='o#' \
            or cid=='op':
                pos = dt if cid=='o#' else pos
                if not(0<=pos<len(lst)):                    return []
                path    = lst[pos]
                if os.path.isdir(path):
                    path= app.dlg_file(True, '', path, '')
                    if not path:                            return []
                if not os.path.isfile(path):                return (app.msg_status(f(_('Not exist: {}'), path)), [])[1]
                app.file_open(path)
                return [] if scam=='s' else None            # Auto-close
            # Modify
            if False:pass
            elif cid=='ac':
                fn      = ed.get_filename('*')
                if fn and not any([os.path.samefile(fn, f) for f in lst]):
                    lst+= [fn]
                    pos = len(lst)-1
                else:                                       return []
            elif cid=='de':
                if not(0<=pos<len(lst)):                    return []
                del lst[pos]
                pos     = min(max(0, pos), len(lst)-1)
            elif cid=='br':
                fn      = app.dlg_dir('') if scam=='s' else app.dlg_file(True, '', '', '')
                if fn is None:                              return []
                if fn and os.path.basename(fn).upper()=='SynFav.ini'.upper():
                    import_SynFav(fn, files)
                elif fn and not any([os.path.samefile(fn, f) for f in lst]):
                    lst+= [fn]
                    pos = len(lst)-1
                else:                                       return []
            elif cid in ('up', 'dn') and len(lst)>1:
                newp    = pos + (-1 if cid=='up' else +1)
                if 0<=newp<len(lst):
                    lst[pos], lst[newp] = lst[newp], lst[pos]
                    pos    = newp
            return d(ctrls=d(fs=d(items=get_its(files, fo)  ,val=pos if 0==its else ag.val('fs'))
                            ,ps=d(items=get_its(projs, fo)  ,val=pos if 1==its else ag.val('ps')) )
                    ,fid='fs' if 0==its else 'ps')

            return []
            
        def do_keys(ag, key, data=''):
            scam    = ag.scam()
            if scam in ('a', 'c') and ord('1')<=key<=ord('9'): # Alt+1..9 or Ctrl+1..9
                return do_act(ag, 'o#', key-ord('1'))
            return []
        
        open_h  = _('Open file/project and close dialog.'
                 '\rShift+Click to open without dialog closing')
        brow_h  = _('Choose file to append.'
                 '\rShift+Click to choose folder')
        itts    = [_('Files'), _('Projects')]
        BH      = app.app_proc(app.PROC_GET_GUI_HEIGHT, 'button')
        ag      = DlgAg(
            form    =d(  cap=_('Favorites 1.2')
                        ,w=500, h=320
                        ,on_key_down=do_keys
                        ,frame='resize')
        ,   ctrls   =d(
          ts=d(tp='tabs',y=5   ,x=5 ,r=-5-110-5,h=BH    ,items=itts             ,a='b.r>'   ,on=do_act
        ),fs=d(tp='libx',y=5+BH,x=5 ,r=-5-110-5,b=-10-BH,items=itfs             ,a='b.r>'   ,vis=itab==0
        ),ps=d(tp='libx',y=5+BH,x=5 ,r=-5-110-5,b=-10-BH,items=itps             ,a='b.r>'   ,vis=itab==1
        ),op=d(tp='bttn',y=5+BH     ,r=-5       ,w=110  ,cap=_('&Open')         ,a=  '>>'   ,on=do_act    ,en=enopen    # &o    default
                                                        ,hint=open_h,def_bt=True                                                        
        ),ac=d(tp='bttn',y=5+ 70    ,r=-5       ,w=110  ,cap=_('&Add opened')   ,a=  '>>'   ,on=do_act    ,en=enaddc    # &a
        ),br=d(tp='bttn',y=5+100    ,r=-5       ,w=110  ,cap=_('Add&...')       ,a=  '>>'   ,on=do_act                  # &.
                                                        ,hint=brow_h                                                        
        ),de=d(tp='bttn',y=5+145    ,r=-5       ,w=110  ,cap=_('&Delete')       ,a=  '>>'   ,on=do_act                  # &d
        ),up=d(tp='bttn',y=5+190    ,r=-5       ,w=110  ,cap=_('Move &up')      ,a=  '>>'   ,on=do_act                  # &u
        ),dn=d(tp='bttn',y=5+220    ,r=-5       ,w=110  ,cap=_('Move do&wn')    ,a=  '>>'   ,on=do_act                  # &w
        ),fo=d(tp='chck',tid='cl'   ,x=5        ,w=150  ,cap=_('Show &paths')   ,a='..'     ,on=do_act                  # &p
        ),he=d(tp='bttn',tid='cl'   ,x=-110-35  ,w= 25  ,cap=_('&?')            ,a='..>>'   ,on=do_act                  # &?
        ),cl=d(tp='bttn',y=-5-BH    ,x=-110-5   ,w=110  ,cap=_('Close')         ,a='..>>'   ,on=CB_HIDE        
                    ))
        ,   fid     ='fs'   if itab==0 and itfs                 else
                     'ps'   if itab==1 and itps                 else
                     'ac'   if itab==0 and ed.get_filename('*') else
                     'brow'
        ,   vals    =d(ts=itab
                      ,fo=fold
                      ,fs=flast
                      ,ps=plast
                      )
        ,   opts    =d(negative_coords_reflect=True)
        )
        pass;                  #ag.gen_repro_code('repro_dlg_fav.py')
        ag.show(on_exit=lambda ag_:save_fav_data(
            d(fv_tab    =ag_.val('ts')
             ,fv_flast  =ag_.val('fs')
             ,fv_plast  =ag_.val('ps')
             ,fv_fold   =ag_.val('fo')
             ,fv_files  =files
             ,fv_projs  =projs
        )))
       #def dlg

    def dlg_help(self):
        app.msg_box(_('• Quick opening.'
                    '\rUse Alt+1, Alt+2, ..., Alt+9'
                    '\ror Ctrl+1, Ctrl+2, ..., Ctrl+9'
                    '\rto quickly open item by its index (1, 2, ... 9).'
                    '\r '
                    '\r• Import favorites from SynWrite. '
                    '\rTo import favorites list from SynWrite, browse for file "SynFav.ini".'
                    '\rThis file is located in the "Settings" subfolder of SynWrite.'
                    ), app.MB_OK)
       #def dlg_help
   #class Command

'''
ToDo
[+][at-kv][20jun16] Moved from cuda_ext
'''
