# -*- coding: utf-8 -*-
# Setup VIM: ex: noet ts=2 sw=2 :
"""
    MoinMoin - Dokuwiki Formatter

    @copyright: 2000, 2001, 2002 by Jürgen Hermann <jh@web.de>
    @copyright: 2011-2012 Elan Ruusamäe <glen@delfi.ee>
    @license: GNU GPL, see COPYING for details.
"""

from xml.sax import saxutils
from MoinMoin.formatter import FormatterBase
from MoinMoin import config
from MoinMoin.Page import Page
from types import *
from MoinMoin import log

logging = log.getLogger(__name__)

# TODO: let base class MoinMoin/formatter/base.py handle not implemented methods

class Formatter(FormatterBase):
    """
        Send Dokuwiki formatted data.
    """

    hardspace = '&nbsp;'
#   hardspace = ' '

    def __init__(self, request, **kw):
        apply(FormatterBase.__init__, (self, request), kw)
        self._current_depth = 1
        self._base_depth = 0
        self.in_pre = 0
        self.in_table = 0
        self._text = None # XXX does not work with links in headings!!!!!
        self.randomID= None
        self.list_depth = 0
        self.list_type = ' '

    def setRandomID(self,ID):
        self.randomID = str(ID)

    def _escape(self, text, extra_mapping={"'": "&apos;", '"': "&quot;"}):
        return saxutils.escape(text, extra_mapping)

    def startDocument(self, pagename):
        encoding = config.charset
        return '<?xml version="1.0" encoding="%s"?>\n<s1 title="%s">' % (
            encoding, self._escape(pagename))

    def endDocument(self):
        result = ""
        while self._current_depth > 1:
            result += "</s%d>" % self._current_depth
            self._current_depth -= 1
        return result + '</s1>'

    def lang(self, on, lang_name):
        return ('<div lang="">' % lang_name, '</div>')[not on]

    def sysmsg(self, on, **kw):
        return ('<sysmsg>', '</sysmsg>')[not on]

    def rawHTML(self, markup):
        #return '<html>' + markup + '</html>'
        return ''

    def pagelink(self, on, pagename='', page=None, **kw):
        if on:
            return '[[:' + ":".join(pagename.split("/")) + "|"
        else:
            return ']]'

    def interwikilink(self, on, interwiki='', pagename='', **kw):
        if on:
            if interwiki == 'Self':
                return self.pagelink(on, pagename, **kw)
            interwikis = {
                'WikiPedia':'wp',
                'FrWikiPedia':'wpfr',
                'DeWikiPedia':'wpde',
                'MetaWikiPedia':'wpmeta'
                }
            if interwiki in interwikis:
                return '[[%s>%s|' % (interwikis.get(interwiki), pagename)
            return '[[%s>%s|' % (interwiki, pagename)
        else:
            return ']]'

    def url(self, on, url='', css=None, **kw):
        return ('[[%s|' % (self._escape(url)), ']]')[not on]

    def attachment_link(self, on, url=None, querystr=None, **kw):
        if on:
            return '{{ %s | ' % (self.randomID+url)
        else: 
            return ' }}'

    def attachment_image(self, url, **kw):
        return '{{%s|}}' % (self.randomID+url,)

    def attachment_drawing(self, url, text, **kw):
        return '{{%s|%s}}' % (self.randomID+url, text)

    def text(self, text, **kw):
        self._did_para = 0
        if self._text is not None:
            self._text.append(text)
        return text

    def rule(self, size=0, **kw):
        # size not supported
        if size >= 4:
            return '----\n'
        else:
            return '-' * size + '\n'

    def icon(self, type):
        return '<icon type="%s" />' % type

    def strong(self, on, **kw):
        return ['**', '**'][not on]

    def emphasis(self, on, **kw):
        return ['//', '//'][not on]

    def highlight(self, on, **kw):
        return ['**', '**'][not on]

    def number_list(self, on, type=None, start=None, **kw):
        # list type not supported
        if on:
            self.list_depth += 1
            self.list_type = '-'
        else:
            self.list_depth -= 1
            self.list_type = ' '

        return ['', '\n'][on]

    def bullet_list(self, on, **kw):
        if on:
            self.list_depth += 1
            self.list_type = '*'
        else:
            self.list_depth -= 1
            if self.list_depth <= 0:
                self.list_type = ' '

        return ['', '\n'][on]

    # generic transclude/include:
    def transclusion(self, on, **kw):
        return ''

    def transclusion_param(self, **kw):
        return ''

    def listitem(self, on, **kw):
        # somewhy blockquote uses "listitem" call
        return [(' ' * self.list_depth * 2) + self.list_type + ' ', '\n'][not on]

    def code(self, on, **kw):
        """ `typewriter` or {{{typerwriter}}, for code blocks i hope codeblock works """
        return ["''%%", "%%''"][not on]

    def sup(self, on, **kw):
        return ['<sup>', '</sup>'][not on]

    def sub(self, on, **kw):
        return ['<sub>', '</sub>'][not on]

    def strike(self, on, **kw):
        return ['<del>', '</del>'][not on]

    def small(self, on, **kw):
        #https://www.dokuwiki.org/plugin:wrap
        return ['<wrap lo>', '</wrap>'][not on]

    def big(self, on, **kw):
        #https://www.dokuwiki.org/plugin:wrap
        return ['<wrap hi>', '</wrap>'][not on]

    def preformatted(self, on, **kw):
        FormatterBase.preformatted(self, on)
        result = ''
        if self.in_p:
            result = self.paragraph(0)
        return result + ['<code>', '</code>\n'][not on]

    def paragraph(self, on, **kw):
        FormatterBase.paragraph(self, on)
        if self.in_table or self.list_depth:
            return ''
        return ['', '\n\n'][not on]

    def linebreak(self, preformatted=1):
        return ['\n', '\\\n'][not preformatted]

    def heading(self, on, depth, **kw):
        # heading depth reversed in dokuwiki
        heading_depth = 7 - depth

        if on:
            return u'%s ' % (u'=' * heading_depth)
        else:
            return u' %s\n' % (u'=' * heading_depth)

    def table(self, on, attrs={}, **kw):
        if on:
            self.in_table = 1
        else:
            self.in_table = 0
        return ['', '\n'][not on]

    def table_row(self, on, attrs={}, **kw):
        return ['\n', '|'][not on]

    def table_cell(self, on, attrs={}, **kw):
        return ['|', ''][not on]

    def anchordef(self, id):
        # https://www.dokuwiki.org/plugin:anchor
        return '{{anchor:'+id+'}}'

    def anchorlink(self, on, name='', **kw):
        # kw.id not supported, we hope the anchor matches existing heading on page
        return ('[[#', ']]') [not on]

    def underline(self, on, **kw):
        return ['__', '__'][not on]

    def definition_list(self, on, **kw):
        # https://www.dokuwiki.org/plugin:definitionlist
        result = ''
        if self.in_p:
            result = self.paragraph(0)
        return result

    def definition_term(self, on, compact=0, **kw):
		#MoinMoin does no wiki markup in DL-Terms
        return ['  ;%%', '%%\n'][not on]

    def definition_desc(self, on, **kw):
        return ['  :', '\n'][not on]

    def image(self, src=None, **kw):
        valid_attrs = ['src', 'width', 'height', 'alt', 'title']

        url = src
        if '?' in url:
            url += '&'
        else:
            url += '?'

        attrs = {}
        for key, value in kw.items():
            if key in valid_attrs:
                attrs[key] = value

        # TODO: finish this
        if attrs.has_key('width'):
            url += attrs['width']

        return '{{' + url + '}}'

    def code_area(self, on, code_id, code_type='code', show=0, start=-1, step=-1,msg=None):
        syntax = ''
        # switch for Python: http://simonwillison.net/2004/may/7/switch/
        try:
            syntax = {
                'ColorizedPython': 'python',
                'ColorizedPascal': 'pascal',
                'ColorizedJava': 'java',
                'ColorizedCPlusPlus': 'cpp',
            }[code_type]
        except KeyError:
            pass

        return ('<code %s>' % syntax , '</code>')[not on]

    def code_line(self, on):
        return ('', '\n')[on]

    def code_token(self, on, tok_type):
        # not supported
        return ''

    def comment(self, text):
        # real comments (lines with two hash marks)
        if text[0:2] == '##':
            # https://www.dokuwiki.org/plugin:comment
            comment = text[2:].strip()
            if len(comment)>1:
                return "/* %s */\n" % text[2:].strip()
            return '\n'

        # Some kind of Processing Instruction
        # http://moinmo.in/HelpOnProcessingInstructions
        tokens = text.lstrip('#').split(None, 1)
        if tokens[0] in ('language', 'format', 'refresh'):
            return ''

        if tokens[0] == 'acl':
            # TODO: fill acl.auth.php
            logging.info('SKIPPING ACL: %s', text)
            return ''

        if tokens[0] == 'deprecated':
            return '<note warning>This page is deprecated</note>\n'

        if tokens[0] == 'redirect':
            return text + "\n"

        if tokens[0] == 'pragma':
            # TODO: can do 'description' via 'meta' dokuwiki plugin
            pargs = tokens[1].split(None, 1)
            if pargs[0]=='section-numbers':
                return '/* meta: %s */' % tokens
            logging.info('SKIPPING PRAGMA: %s', tokens)
            #return "/* pragma: %s */\n" % " ".join(tokens[1:])
            return ''

        #return "/* %s */\n" % text.lstrip('#')
        return ''


    def macro(self, macro_obj, name, args,markup):
        def email(args):
            mail = args.replace(' AT ', '@')
            mail = mail.replace(' DOT ', '.')
            return '[[%s|%s]]' % (mail, args)

        def showAttachedFiles(args):
            args = args.split(',')
            if len(args)>1:
                return '{{ %s | %s }}' % (self.randomID+args[0].strip(), args[1].strip())
            else:
                return ''

        # function which will just do what parent class would
        def inherit(args):
            return apply(FormatterBase.macro, (self, macro_obj, name, args))

        def randomQuote(args):
            # https://www.dokuwiki.org/plugin:xfortune
            return '{{xfortune>quote:'+args+'.txt}}'

        def monthcal(args):
            # https://www.dokuwiki.org/plugin:monthcal
            selfname = self.page.page_name
            return '{{monthcal:create_links=short,namespace='+selfname.replace('/',':')+'}}'

        def navigation(args):
            # https://www.dokuwiki.org/plugin:alphaindex
            selfname = self.page.page_name
            args = args.split(',')
            if len(args)>0:
                try:
                    result = {
                      'slides': '[<>]',
                      'children': '{{alphaindex>:%s#1|nons incol}}' % selfname.replace('/',':'),
                      'siblings': '{{alphaindex>.#1|nons incol}}',
                      'slideshow': '/* no support for slideshow navigation */'
                    }[args[0].strip()]
                except KeyError:
                    result = '/* Unknown Navigation: %s #%s#*/' % args, args[0].strip()
            else:
                result = '/* Unsupported Navigation: %s */' % args
            return result

        def footnote(args):
            return '((%s))' % args

        def dateTimeMacro(args):
            #https://www.dokuwiki.org/plugin:date
            #args = args.split(',');
            return '{{date>%%c|timestamp=strtotime("%s")|locale=de}}' % args

        def dateMacro(args):
            #https://www.dokuwiki.org/plugin:date
            #args = args.split(',');
            return '{{date>%%x|timestamp=strtotime("%s")|locale=de}}' % args

        def includeMacro(args):
            #https://www.dokuwiki.org/plugin:include
            #logging.info('Include(%s)' % args)
            args = map(unicode.strip, args.split(','));
            #dokupage = ":".join(pagename.split("/"))
            if len(args)==1:
                return '{{page>%s&nodate}}' % ":".join(args[0].split("/"))
            elif(u'titlesonly' in args):
                #https://www.dokuwiki.org/plugin:changes
                #https://www.dokuwiki.org/plugin:pagelist
                selfname = self.page.page_name
                selfNs = ":".join(selfname.split("/")).lower()
                pairs = [arg.split('=') for arg in args]
                # attrs = {}
                # for key, value in pairs:
                    # attrs[key] = value
                #logging.info('pairs:"%s"' % pairs)

                incName = ''#pairs[0]
                incCount = -1
                incTitlesOnly = False
                notNamedParam = 0
                for pair in pairs:
                    if len(pair)==1:
                        if u'titlesonly'==pair:
                            notNamedParam = -1
                            incTitlesOnly = True
                        elif notNamedParam >=0:
                            if notNamedParam==0:
                                incName = pairs[notNamedParam]
                            notNamedParam += 1;
                    else:
                        notNamedParam = -1
                        if u'items'==pair[0]:
                            incCount = int(pair[1])

                resultArgs = '-h1 -textPages=""'
                #(keys,values) = map()
                if incCount > 0:
                    resultArgs += ' -idAndTitle -simpleList -sortId -nbItemsMax=%d' % incCount
                else:
                    resultArgs += ' -nbCol=2'

                ##<nspages fortran:mailarchiv -pregPagesOn="/2.*/" -h1 -nbCol=2 -textPages="">
                ## Lister der letzten 10 Mails:
                ##<nspages .:mailarchiv -nbItemsMax=10 -sortId -simpleList -idAndTitle -reverse -h1 -nbCol=1 -textPages=""> 
                if incName[0]=='^':
                    nspagedelim = incName.rfind('/')
                    ns = ":".join(incName[1:nspagedelim].split('/')).lower()
                    incPageReg = incName[(nspagedelim+1):]
                    resultArgs += ' -pregPagesOn="/^%s/"' % incPageReg
                else:
                    ns = selfNs

                return '<nspages %s %s>' % (ns, resultArgs)

            else:
                logging.info('UNSUPPORTED INCLUDE "%s"' % args)
                return '/* Unsupported Include: %s */' % args

        def fullsearch(args):
            #args=None >> {searchform ns=}
            #args='' >> {{backlinks>.}}
            #args!='' >> {{search><args>}}
            #ignore special searches. see MoinMoin page "HilfeZumSuchen"
            if args is None:
                return '{searchform ns=}'
            elif ':' in args or ' ' in args:
                logging.info('UNSUPPORTED SEARCH %s(%s)' % (name, args))
                return '/* Unsupported Search %s(%s). may be backlinks plugin will help */' % (name, args)
            elif args=='':
                return '{{backlinks>.}}'
            elif name=='PageList':
                return '{{backlinks>%s}}' % ":".join(args.split('/')).lower();
            else:
                logging.info('UNSUPPORTED SEARCH %s(%s)' % (name, args))
                return '/* Unsupported Search %s(%s) */' % (name, args)

        try:
            lookup = {
                'BR' : ' \\\\ ',
                'br' : ' \\\\ ',
                'MailTo' : email,
                'GetText' : args,
                'ShowSmileys' : inherit,
                'ShowAttachedFiles' : showAttachedFiles,
                'Include' : includeMacro,
                #no real fulltext search!
                'FullSearch' : fullsearch,
                'FullSearchCached' : fullsearch,
                'PageList' : fullsearch,
                'MonthCalendar' : monthcal,
                'Navigation' : navigation,
                'TableOfContents' : '',
                'RandomQuote': randomQuote,
                'Anchor': inherit,
                'Action': inherit,
                'Icon': inherit,
                'FootNote': footnote,
                'Date': dateMacro,
                'DateTime': dateTimeMacro
            }[name]
        except KeyError:
            logging.info('UNDEFINED MACRO "%s"' % name)
            lookup = '/* UndefinedMacro: %s(%s) */' % (name, args)

        if type(lookup) == FunctionType:
            text = lookup(args)
        else:
            text = lookup
        return text

    def smiley(self, text):
        try:
            # https://www.dokuwiki.org/devel:smileys.conf
            return {
                # note: reverse sorted so that longer smileys get matched first
                'X-('   : ':-X',
                '{X}'   : ':!:',
                '{*}'   : '<ubu>',
                '(./)'  : u'✓',
                ':))'   : ':-P',
                ':-))'  : ':-P',
                ':-?'   : ':-P',
                ':o'    : ':-o',
                '{OK}'  : ':!:',
                '{o}'   : '<circ>',
                '{i}'   : ':!:',
                ':D'    : ':-D',
                'B)'    : '8-)',
                'B-)'   : '8-)',
                '{3}'   : '<3>',
                '{2}'   : '<2>',
                '{1}'   : '<1>',
                '(!)'   : ':!:',
                '/!\\'  : ':!:',
                ':\\'   : ':-\\',
                ':))'   : ':-)',
                ':)'    : ':-)',
                ':('    : ':-(',
                ':-))'  : ':-)',
                ':-)'   : ':-)',
                ':-('   : ':-(',
                ';)'    : ';-)',
                '|)'    : ':-|',
                '|-)'   : ':-|',
                '>:>'   : '^_^',
                '<!>'   : ':!:',
                '<:('   : ':-?',
            }[text]
        except KeyError:
            return text
