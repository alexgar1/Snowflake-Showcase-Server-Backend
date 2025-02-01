/**  
 * A bunch of helpful functions for our snowflake page
 * Konstantin Shkurko
 * 02.22.12
 */

var t;
var timer_is_on = 0;
var t2;
var c;
var prevTimeOut    = 5000;
var prevTimeOutSet = 1;

	
function hasClass(el, name) {
	return new RegExp('(\\s|^)'+name+'(\\s|$)').test(el.className);
}
function removeClass(el, name) {
	if (hasClass(el, name)) {
		el.className=el.className.replace(new RegExp('(\\s|^)'+name+'(\\s|$)'),' ').replace(/^\s+|\s+$/g, '');
	}
}
function addClass(el, name) {
	if (!hasClass(el, name)) { el.className += (el.className ? ' ' : '') +name; }
}
function setTimeLeft( val ) {
/*	elem = document.getElementById('timeLeft');
	if( 'textContent' in elem ) {
		elem.textContent = val;
	} else if( 'innerText' in elem ) {
		elem.innerText = val;
	}
*/
	// using jquery (must be included beforehand)
	$('#timeLeft').text( val );
}

function doTimer() {

	// check if we've started a slideshow already -> stop countdown
	//if( $('#lblShow') && $('#lblShow').is(':visible') )
	//	timedRefresh( 0 );

	// initiate the next timer tick
	if( timer_is_on ) {
		c = c - 1;
		setTimeLeft( "in " + c + " sec" );
		t2 = setTimeout( "doTimer()", 1000 );
	}
}

function timedRefresh( timeOutPeriod, flagToIgnoreTOValue ) {
	refOffObj = document.getElementById('refreshOff');
	refOnObj  = document.getElementById('refreshOn');
	if( !refOffObj || !refOnObj ) {
		return;
	}
	if( timeOutPeriod == 0 ) {
		clearTimeout( t );
		addClass( document.getElementById('refreshOff'), 'refreshActive' );
		removeClass( document.getElementById('refreshOn'), 'refreshActive' );

		setTimeLeft( "never" );
		clearTimeout( t2 );
		timer_is_on = 0;
	}
	else if( !hasClass(document.getElementById('refreshOn'), 'refreshActive') ) {
		removeClass( document.getElementById('refreshOff'), 'refreshActive' );
		addClass( document.getElementById('refreshOn'), 'refreshActive' );
		t = setTimeout( "window.location.reload()", timeOutPeriod );

		timer_is_on = 1;
		c  = timeOutPeriod/1000;
		setTimeLeft( "in " + c + " sec" );
		t2 = setTimeout( "doTimer()", 1000 );
	}
	if( typeof flagToIgnoreTOValue == 'undefined' || flagToIgnoreTOValue == 0 ) {
		prevTimeOut    = timeOutPeriod;
		prevTimeOutSet = 1;
	}
}

function toggleTimedRefresh( turnTimerOff ) {
	if( turnTimerOff ) {
		timedRefresh( 0, 1 );
	}
	else if( prevTimeOutSet == 1 ) {
		timedRefresh( prevTimeOut, 1 );
	}
}

function documentLoaded( timeOutPeriod ) {
	// to test functionality -> opens an image with id="img1"
	//$('#img1').trigger('click');
	
	// check if we already have a preview window open
	if( $('#lbCenter').length>0 && $('#lbCenter').is(':visible') ) {
		prevTimeOut    = timeOutPeriod;
		prevTimeOutSet = 1;
	}
	// have we already clicked off?
	else if( hasClass(document.getElementById('refreshOff'), 'refreshActive') ) {
	}
	else {
		timedRefresh( timeOutPeriod );
	}
}