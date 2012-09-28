(function ($, undefined) {
	$(function () {
		$('#choices').on('keyup', 'li input', function () {
			var $self = $(this);
			var $parent = $self.parent();
			if ($parent.is(':last-child') && $self.val().length > 0) {
				var newLi = $parent.clone();
				$parent.after(newLi);
				newLi.find('input').val('').attr({'name': 'choices-' + newLi.index(), 'id': 'choices-' + newLi.index()});
			}
		});
	});
})(Zepto);
