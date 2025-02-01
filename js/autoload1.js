// AUTOLOAD CODE BLOCK (MAY BE CHANGED OR REMOVED)
if (!/android|iphone|ipod|series60|symbian|windows ce|blackberry/i.test(navigator.userAgent)) {
	jQuery(function($) {
		$("a[rel^='lightbox']").slimbox({loop: true}, 
				function(el) { return [el.rev || el.href, el.title]; }, 
				function(el) { return (this == el) || ((this.rel.length > 8) && (this.rel == el.rel)); });
	});
}