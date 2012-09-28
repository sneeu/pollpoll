(function ($, undefined) {
	function colours(start, end, number) {
		var i, s, e, r = [], steps = [];

		function d2h(d) {return d.toString(16);}
		function h2d(h) {return parseInt(h,16);}
		function lpad(str, padding, len) {
			if (str.length >= len) {
				return str;
			}
			return lpad(padding + str, padding, len);
		}

		s = $.map([start.substr(0, 2), start.substr(2, 2), start.substr(4, 2)], h2d);
		e = $.map([end.substr(0, 2), end.substr(2, 2), end.substr(4, 2)], h2d);

		step = [];
		for (i = 0; i < s.length; i++) {
			step.push((e[i] - s[i]) / (number - 1))
		}

		for (i = 0; i < number; i++) {
			r.push('#' + $.map(
				[s[0] + step[0] * i, s[1] + step[1] * i, s[2] + step[2] * i]
				, function (n) {return lpad(d2h(Math.floor(n)), '0', 2);}).join(''));
		}
		return r;
	}

	$(function () {
		var $votes = $('#vote .votes');
		var theColours = colours('cff09e', '3b8686', $votes.size());

		var sum = $votes.reduce(function (memo, item, index, array) {
			return Math.max(memo, parseInt($(item).text()));
		}, 0);

		$votes.each(function (index, item) {
			var $self = $(this);
			$self.css({
				'background': theColours[index],
				'width': (parseInt($self.text()) / sum) * 24 + 'em'
			});
		});
	});
})(Zepto);
