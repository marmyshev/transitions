# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2013 Raoul Snyman                                        #
# Portions copyright (c) 2008-2013 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Erik Lundin, Edwin Lunando, Brian T. Meyer.   #
# Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias Põldaru,          #
# Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,             #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Dave Warnock,              #
# Frode Woldsund, Martin Zibricky, Patrick Zimmermann                         #
# --------------------------------------------------------------------------- #
# This program is free software; you can redistribute it and/or modify it     #
# under the terms of the GNU General Public License as published by the Free  #
# Software Foundation; version 2 of the License.                              #
#                                                                             #
# This program is distributed in the hope that it will be useful, but WITHOUT #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or       #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for    #
# more details.                                                               #
#                                                                             #
# You should have received a copy of the GNU General Public License along     #
# with this program; if not, write to the Free Software Foundation, Inc., 59  #
# Temple Place, Suite 330, Boston, MA 02111-1307 USA                          #
###############################################################################

import logging

from PyQt4 import QtWebKit

from openlp.core.lib.theme import BackgroundType, BackgroundGradientType, VerticalType, HorizontalType

log = logging.getLogger(__name__)

HTMLSRC = u"""
<!DOCTYPE html>
<html>
<head>
<title>OpenLP Display</title>
<style>
*{
    margin: 0;
    padding: 0;
    border: 0;
    overflow: hidden;
    -webkit-user-select: none;
}
body {
    %s;
}
.size {
    position: absolute;
    left: 0px;
    top: 0px;
    width: 100%%;
    height: 100%%;
}
#black {
    z-index: 8;
    background-color: black;
    display: none;
}
#bgimage {
    z-index: 1;
}
#image {
    z-index: 2;
}
%s
#footer {
    position: absolute;
    z-index: 6;
    %s
}
/* lyric css */
%s
sup {
    font-size: 0.6em;
    vertical-align: top;
    position: relative;
    top: -0.3em;
}

#frame1{
	background:maroon;
}
#frame2{
	background:blue
}
#screen{
	height:440px;
	width:720px;
	overflow:hidden;
	position:relative;
}

.frame{
	height:540px;
	width:720px;
    left:0px;
    right0px;
	position:absolute;
	overflow:hidden;
}
.frame h1{margin:auto; display:block; font-size:58px; color:#fff;}
</style>
<script src=/Users/dmiriy/Develop/js/jquery-1.7.2.min.js></script>
<script>
    var current_frame_id = 'frame1';
    var next_frame_id = 'frame2';
	var animation_effect = 'FadeInOut';
	var width = 1024;
	var height = 786;
    var timer = null;
    var transition = %s;
    %s

    function show_image(src){
        var img = document.getElementById('image');
        img.src = src;
        if(src == '')
            img.style.display = 'none';
        else
            img.style.display = 'block';
    }

    function show_blank(state){
        var black = 'none';
        var lyrics = '';
        switch(state){
            case 'theme':
                lyrics = 'hidden';
                break;
            case 'black':
                black = 'block';
                break;
            case 'desktop':
                break;
        }
        document.getElementById('black').style.display = black;
        document.getElementById('lyricsmain').style.visibility = lyrics;
        document.getElementById('image').style.visibility = lyrics;
        outline = document.getElementById('lyricsoutline')
        if(outline != null)
            outline.style.visibility = lyrics;
        shadow = document.getElementById('lyricsshadow')
        if(shadow != null)
            shadow.style.visibility = lyrics;
        document.getElementById('footer').style.visibility = lyrics;
    }

    function show_footer(footertext){
        document.getElementById('footer').innerHTML = footertext;
    }

    function show_text(newtext){
        var match = /-webkit-text-fill-color:[^;\"]+/gi;
        if(timer != null)
            clearTimeout(timer);
        /*
        QtWebkit bug with outlines and justify causing outline alignment
        problems. (Bug 859950) Surround each word with a <span> to workaround,
        but only in this scenario.
        */
        var txt = document.getElementById('lyricsmain');
        if(window.getComputedStyle(txt).textAlign == 'justify'){
            var outline = document.getElementById('lyricsoutline');
            if(outline != null)
                txt = outline;
            if(window.getComputedStyle(txt).webkitTextStrokeWidth != '0px'){
                newtext = newtext.replace(/(\s|&nbsp;)+(?![^<]*>)/g,
                    function(match) {
                        return '</span>' + match + '<span>';
                    });
                newtext = '<span>' + newtext + '</span>';
            }
        }
        text_fade('lyricsmain', newtext);
        text_fade('lyricsoutline', newtext);
        text_fade('lyricsshadow', newtext.replace(match, ''));
        if(text_opacity() == 1) return;
        timer = setTimeout(function(){
            show_text(newtext);
        }, 100);
    }
    
    function show_next(next_item){
		/*
		Show next frame
		*/
		var current_frame = document.getElementById(current_frame_id);
		var next_frame = document.getElementById(next_frame_id);
		current_frame.style.opacity = 1;
		next_frame.style.opacity = 0;
		next_frame.innerHTML = next_item;
		if(!transition){
            no_animation(current_frame, next_frame);
			change_frames(current_frame_id, next_frame_id);
			return;
        }
		if(timer != null)
            clearTimeout(timer);
		switch(animation_effect){
            case 'FadeInOut':
				animation_fadeinout(current_frame, next_frame, 100);
				change_frames(current_frame_id, next_frame_id);
				break;
			case 'FadeIn':
                animation_fadein(current_frame, next_frame, 100);
				change_frames(current_frame_id, next_frame_id);
				break;
            case 'Left':
				current_frame.style.left = '0px';
				next_frame.style.left = '0px';
                animation_moveleft(current_frame, next_frame, 10);
				change_frames(current_frame_id, next_frame_id);
				break;
            case 'Right':
				animation_fadeinout(current_frame, next_frame, 200);
				change_frames(current_frame_id, next_frame_id);
                break;
        }
	}

	function change_frames(current_id, next_id){
		var temp = current_frame_id;
		current_frame_id = next_frame_id;
		next_frame_id = temp;
	}

	function no_animation(current_frame, next_frame){
		current_frame.style.opacity = 0;
		next_frame.style.opacity = 1;
	}

	function animation_fadeinout(current_frame, next_frame, delay){
		/*
		Animation at first fade out current frame, then fade in next frame
		*/
		if(parseFloat(current_frame.style.opacity) > 0.2){
			current_frame.style.opacity = parseFloat(current_frame.style.opacity) - 0.1;
			timer = window.setTimeout(function(){animation_fadeinout(current_frame, next_frame, delay)}, delay);
			return;
		}else if(parseFloat(next_frame.style.opacity) <= 1){
			next_frame.style.opacity = parseFloat(next_frame.style.opacity) + 0.1;
			timer = window.setTimeout(function(){animation_fadeinout(current_frame, next_frame, delay)}, delay);
			return;
		}
		current_frame.style.opacity = 0;
		timer = null;
	}

	function animation_fadein(current_frame, next_frame, delay){
		/*
		Animation fade in next frame, and then hide current
		*/
		if(parseFloat(next_frame.style.opacity) <= 1){
			next_frame.style.opacity = parseFloat(next_frame.style.opacity) + 0.1;
			timer = window.setTimeout(function(){animation_fadeinout(current_frame, next_frame, delay)}, delay);
			return;
		}
		current_frame.style.opacity = '0';
		timer = null;
	}

	function animation_moveleft(current_frame, next_frame, delay){
		/*
		Animation move current frame and next frame from right to left
		*/

		if(parseInt(current_frame.style.left) == 0){
			next_frame.style.left = width + 'px';
		}
		next_frame.style.opacity = '1';
		current_frame.style.opacity = '1';

		var move = parseInt(next_frame.style.left) - 10;
		if(move < 0){
			move = 0;
		}
		next_frame.style.left = move + 'px';
		current_frame.style.left = parseInt(current_frame.style.left) - 10 + 'px';

		if(parseInt(next_frame.style.left) > 0){
			timer = window.setTimeout(function(){animation_moveleft(current_frame, next_frame, delay)}, delay);
			return;
		}
		timer = null;
		current_frame.style.opacity = '0';
		current_frame.style.left = '0px';
	}


    function text_fade(id, newtext){
        /*
        Using -webkit-transition: opacity 1s linear; would have been preferred
        but it isn't currently quick enough when animating multiple layers of
        large areas of large text. Therefore do it manually as best we can.
        Hopefully in the future we can revisit and do more interesting
        transitions using -webkit-transition and -webkit-transform.
        However we need to ensure interrupted transitions (quickly change 2
        slides) still looks pretty and is zippy.
        */
        var text = document.getElementById(id);
        if(text == null) return;
        if(!transition){
            text.innerHTML = newtext;
            return;
        }
        if(newtext == text.innerHTML){
            text.style.opacity = parseFloat(text.style.opacity) + 0.3;
            if(text.style.opacity > 0.7)
                text.style.opacity = 1;
        } else {
            text.style.opacity = parseFloat(text.style.opacity) - 0.3;
            if(text.style.opacity <= 0.1){
                text.innerHTML = newtext;
            }
        }
    }

    function text_opacity(){
        var text = document.getElementById('lyricsmain');
        return getComputedStyle(text, '').opacity;
    }

    function show_text_complete(){
        return (text_opacity() == 1);
    }
    function change_frame(){
        if(current_frame == 1){
            var frame = document.getElementById('frame1');
            frame.style.opacity = 0;
            frame = document.getElementById('frame2');
            frame.style.opacity = 1;
            current_frame = 2;
        } else {
            /* var frame = document.getElementById('frame1');
            frame.style.opacity = 1; */
            frame = document.getElementById('frame2');
            frame.style.opacity = 0;
            current_frame = 1;
            var frame= $('#frame1');
            frame.fadeIn(700);
        }
    }
</script>


</head>
<body>
<img id="bgimage" class="size" %s />
<img id="image" class="size" %s />
%s
%s
<div id="footer" class="footer"></div>
<div id="black" class="size"></div>

<div id="screen">
<div class="frame" id="frame2"><h1>2 -</h1></div>
<div class="frame" id="frame1"><h1>- 1</h1></div>
</div>
</body>
</html>
"""


def build_html(item, screen, is_live, background, image=None, plugins=None):
    """
    Build the full web paged structure for display

    ``item``
        Service Item to be displayed

    ``screen``
        Current display information

    ``islive``
        Item is going live, rather than preview/theme building

    ``background``
        Theme background image - bytes

    ``image``
        Image media item - bytes

    ``plugins``
        The List of available plugins
    """
    width = screen[u'size'].width()
    height = screen[u'size'].height()
    theme = item.themedata
    webkit_ver = webkit_version()
    # Image generated and poked in
    if background:
        bgimage_src = u'src="data:image/png;base64,%s"' % background
    elif item.bg_image_bytes:
        bgimage_src = u'src="data:image/png;base64,%s"' % item.bg_image_bytes
    else:
        bgimage_src = u'style="display:none;"'
    if image:
        image_src = u'src="data:image/png;base64,%s"' % image
    else:
        image_src = u'style="display:none;"'
    css_additions = u''
    js_additions = u''
    html_additions = u''
    if plugins:
        for plugin in plugins:
            css_additions += plugin.getDisplayCss()
            js_additions += plugin.getDisplayJavaScript()
            html_additions += plugin.getDisplayHtml()
    html = HTMLSRC % (
        build_background_css(item, width, height),
        css_additions,
        build_footer_css(item, height),
        build_lyrics_css(item, webkit_ver),
        u'true' if theme and theme.display_slide_transition and is_live else u'false',
        js_additions,
        bgimage_src, image_src,
        html_additions,
        build_lyrics_html(item, webkit_ver)
    )
    return html


def webkit_version():
    """
    Return the Webkit version in use.
    Note method added relatively recently, so return 0 if prior to this
    """
    try:
        webkit_ver = float(QtWebKit.qWebKitVersion())
        log.debug(u'Webkit version = %s' % webkit_ver)
    except AttributeError:
        webkit_ver = 0
    return webkit_ver


def build_background_css(item, width, height):
    """
    Build the background css

    ``item``
        Service Item containing theme and location information

    """
    width = int(width) / 2
    theme = item.themedata
    background = u'background-color: black'
    if theme:
        if theme.background_type == BackgroundType.to_string(BackgroundType.Transparent):
            background = u''
        elif theme.background_type == BackgroundType.to_string(BackgroundType.Solid):
            background = u'background-color: %s' % theme.background_color
        else:
            if theme.background_direction == BackgroundGradientType.to_string(BackgroundGradientType.Horizontal):
                background = u'background: -webkit-gradient(linear, left top, left bottom, from(%s), to(%s)) fixed' \
                    % (theme.background_start_color, theme.background_end_color)
            elif theme.background_direction == BackgroundGradientType.to_string(BackgroundGradientType.LeftTop):
                background = u'background: -webkit-gradient(linear, left top, right bottom, from(%s), to(%s)) fixed' \
                    % (theme.background_start_color, theme.background_end_color)
            elif theme.background_direction == BackgroundGradientType.to_string(BackgroundGradientType.LeftBottom):
                background = u'background: -webkit-gradient(linear, left bottom, right top, from(%s), to(%s)) fixed' \
                    % (theme.background_start_color, theme.background_end_color)
            elif theme.background_direction == BackgroundGradientType.to_string(BackgroundGradientType.Vertical):
                background = u'background: -webkit-gradient(linear, left top, right top, from(%s), to(%s)) fixed' % \
                    (theme.background_start_color, theme.background_end_color)
            else:
                background = u'background: -webkit-gradient(radial, %s 50%%, 100, %s 50%%, %s, from(%s), to(%s)) fixed'\
                    % (width, width, width, theme.background_start_color, theme.background_end_color)
    return background


def build_lyrics_css(item, webkit_ver):
    """
    Build the lyrics display css

    ``item``
        Service Item containing theme and location information

    ``webkitvers``
        The version of qtwebkit we're using

    """
    style = u"""
.lyricstable {
    z-index: 5;
    position: absolute;
    display: table;
    %s
}
.lyricscell {
    display: table-cell;
    word-wrap: break-word;
    %s
}
.lyricsmain {
%s
}
.lyricsoutline {
%s
}
.lyricsshadow {
%s
}
    """
    theme = item.themedata
    lyricstable = u''
    lyrics = u''
    lyricsmain = u''
    outline = u''
    shadow = u''
    if theme and item.main:
        lyricstable = u'left: %spx; top: %spx;' % (item.main.x(), item.main.y())
        lyrics = build_lyrics_format_css(theme, item.main.width(), item.main.height())
        # For performance reasons we want to show as few DIV's as possible,
        # especially when animating/transitions.
        # However some bugs in older versions of qtwebkit mean we need to
        # perform workarounds and add extra divs. Only do these when needed.
        #
        # Before 533.3 the webkit-text-fill colour wasn't displayed, only the
        # stroke (outline) color. So put stroke layer underneath the main text.
        #
        # Up to 534.3 the webkit-text-stroke was sometimes out of alignment
        # with the fill, or normal text. letter-spacing=1 is workaround
        # https://bugs.webkit.org/show_bug.cgi?id=44403
        #
        # Up to 534.3 the text-shadow didn't get displayed when
        # webkit-text-stroke was used. So use an offset text layer underneath.
        # https://bugs.webkit.org/show_bug.cgi?id=19728
        if webkit_ver >= 533.3:
            lyricsmain += build_lyrics_outline_css(theme)
        else:
            outline = build_lyrics_outline_css(theme)
        if theme.font_main_shadow:
            if theme.font_main_outline and webkit_ver <= 534.3:
                shadow = u'padding-left: %spx; padding-top: %spx;' % \
                    (int(theme.font_main_shadow_size) + (int(theme.font_main_outline_size) * 2),
                     theme.font_main_shadow_size)
                shadow += build_lyrics_outline_css(theme, True)
            else:
                lyricsmain += u' text-shadow: %s %spx %spx;' % \
                    (theme.font_main_shadow_color, theme.font_main_shadow_size,
                    theme.font_main_shadow_size)
    lyrics_css = style % (lyricstable, lyrics, lyricsmain, outline, shadow)
    return lyrics_css


def build_lyrics_outline_css(theme, is_shadow=False):
    """
    Build the css which controls the theme outline
    Also used by renderer for splitting verses

    ``theme``
        Object containing theme information

    ``is_shadow``
        If true, use the shadow colors instead
    """
    if theme.font_main_outline:
        size = float(theme.font_main_outline_size) / 16
        if is_shadow:
            fill_color = theme.font_main_shadow_color
            outline_color = theme.font_main_shadow_color
        else:
            fill_color = theme.font_main_color
            outline_color = theme.font_main_outline_color
        return u' -webkit-text-stroke: %sem %s; -webkit-text-fill-color: %s; ' % (size, outline_color, fill_color)
    else:
        return u''


def build_lyrics_format_css(theme, width, height):
    """
    Build the css which controls the theme format
    Also used by renderer for splitting verses

    ``theme``
        Object containing theme information

    ``width``
        Width of the lyrics block

    ``height``
        Height of the lyrics block

    """
    align = HorizontalType.Names[theme.display_horizontal_align]
    valign = VerticalType.Names[theme.display_vertical_align]
    if theme.font_main_outline:
        left_margin = int(theme.font_main_outline_size) * 2
    else:
        left_margin = 0
    justify = u'white-space:pre-wrap;'
    # fix tag incompatibilities
    if theme.display_horizontal_align == HorizontalType.Justify:
        justify = u''
    if theme.display_vertical_align == VerticalType.Bottom:
        padding_bottom = u'0.5em'
    else:
        padding_bottom = u'0'
    lyrics = u'%s word-wrap: break-word; ' \
        'text-align: %s; vertical-align: %s; font-family: %s; ' \
        'font-size: %spt; color: %s; line-height: %d%%; margin: 0;' \
        'padding: 0; padding-bottom: %s; padding-left: %spx; width: %spx; height: %spx; ' % \
        (justify, align, valign, theme.font_main_name, theme.font_main_size,
        theme.font_main_color, 100 + int(theme.font_main_line_adjustment), padding_bottom, left_margin, width, height)
    if theme.font_main_outline:
        if webkit_version() <= 534.3:
            lyrics += u' letter-spacing: 1px;'
    if theme.font_main_italics:
        lyrics += u' font-style:italic; '
    if theme.font_main_bold:
        lyrics += u' font-weight:bold; '
    return lyrics


def build_lyrics_html(item, webkitvers):
    """
    Build the HTML required to show the lyrics

    ``item``
        Service Item containing theme and location information

    ``webkitvers``
        The version of qtwebkit we're using
    """
    # Bugs in some versions of QtWebKit mean we sometimes need additional
    # divs for outline and shadow, since the CSS doesn't work.
    # To support vertical alignment middle and bottom, nested div's using
    # display:table/display:table-cell are required for each lyric block.
    lyrics = u''
    theme = item.themedata
    if webkitvers <= 534.3 and theme and theme.font_main_outline:
        lyrics += u'<div class="lyricstable">' \
            u'<div id="lyricsshadow" style="opacity:1" ' \
            u'class="lyricscell lyricsshadow"></div></div>'
        if webkitvers < 533.3:
            lyrics += u'<div class="lyricstable">' \
                u'<div id="lyricsoutline" style="opacity:1" ' \
                u'class="lyricscell lyricsoutline"></div></div>'
    lyrics += u'<div class="lyricstable">' \
        u'<div id="lyricsmain" style="opacity:1" ' \
        u'class="lyricscell lyricsmain"></div></div>'
    return lyrics


def build_footer_css(item, height):
    """
    Build the display of the item footer

    ``item``
        Service Item to be processed.
    """
    style = u"""
    left: %spx;
    bottom: %spx;
    width: %spx;
    font-family: %s;
    font-size: %spt;
    color: %s;
    text-align: left;
    white-space: nowrap;
    """
    theme = item.themedata
    if not theme or not item.footer:
        return u''
    bottom = height - int(item.footer.y()) - int(item.footer.height())
    lyrics_html = style % (item.footer.x(), bottom, item.footer.width(),
        theme.font_footer_name, theme.font_footer_size, theme.font_footer_color)
    return lyrics_html
