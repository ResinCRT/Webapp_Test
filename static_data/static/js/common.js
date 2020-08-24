HTMLElement.prototype.on = function (eventName, selector, handler) {
    let self = this;
    self.addEventListener(eventName, function (e) {
        elements = self.querySelectorAll(selector);
        let target = e.target;
        elements.forEach(item => {
            if (item == target) {
                handler.call(target, e);
            }
        });
    });
}