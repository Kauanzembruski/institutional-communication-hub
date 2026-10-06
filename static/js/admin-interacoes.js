(() => {
    "use strict";

    const modalSelector = "[data-admin-close]";

    function visible(element) {
        return element.getClientRects().length > 0 &&
            getComputedStyle(element).visibility !== "hidden";
    }

    function activeModal() {
        return [...document.querySelectorAll(modalSelector)]
            .filter(visible)
            .sort((a, b) => (Number(getComputedStyle(a).zIndex) || 0) -
                (Number(getComputedStyle(b).zIndex) || 0))
            .pop();
    }

    function close(modal) {
        const callback = window[modal.dataset.adminClose];
        if (typeof callback === "function") {
            callback();
        } else {
            modal.style.display = "none";
        }
    }

    // Capture the press before an opening button can display a new modal.
    document.addEventListener("pointerdown", (event) => {
        if (event.button !== 0) return;
        const modal = activeModal();
        if (!modal) return;
        const overlay = modal.classList.contains("modal") ||
            modal.classList.contains("modal-mensagem");
        if (!modal.contains(event.target) || (overlay && event.target === modal)) {
            close(modal);
        }
    }, true);

    document.addEventListener("keydown", (event) => {
        if (event.isComposing || event.defaultPrevented) return;
        const modal = activeModal();
        if (event.key === "Escape" && modal) {
            event.preventDefault();
            event.stopImmediatePropagation();
            close(modal);
            return;
        }
        if (event.key !== "Enter") return;

        const scope = modal || event.target.closest("[data-admin-submit]");
        if (!scope) return;
        const form = scope.querySelector("form");
        const callback = window[scope.dataset.adminSubmit];
        if (!form && typeof callback !== "function") return;

        // Prevent implicit submission or activation of Cancel/Delete buttons.
        event.preventDefault();
        event.stopImmediatePropagation();
        if (event.repeat) return;
        if (form) {
            const submitter = form.querySelector('button[type="submit"], input[type="submit"], button:not([type])');
            if (!submitter || !submitter.disabled) {
                form.requestSubmit(submitter || undefined);
            }
        } else {
            const fields = [...scope.querySelectorAll("input, select, textarea")];
            if (fields.every((field) => field.reportValidity())) callback();
        }
    }, true);
})();
