// Demo safety guard: resolves the real control text (labels, aria, type, autocomplete)
// before any pointer action, refuses destructive-looking controls and credential fields.
// Clicks and typing are judged on all of a control's text. Drag ends and selects are judged on
// their own name only, so a calendar column or a status menu is not refused because of what
// it contains (an appointment called "Reset sprinkler heads", a "Remove" option).
// The built-in deny list always applies; a plan's denyPattern only adds to it.
// Designed by Legion Code Inc.
const DEFAULT_DENY = "\\b(?:delete|remove|reset|revoke|restart|logout|log\\s*out|sign\\s*out|pay|purchase|transfer|publish|destroy|drop|shutdown)\\b";
const SECRET_FIELD = /password|passcode|passphrase|credential|secret|token|api[-_ ]?key|private[-_ ]?key|one-time-code|\botp\b|\bpin\b/i;
const SECRET_VALUE = /-----BEGIN [A-Z ]*PRIVATE KEY-----|\bAKIA[0-9A-Z]{16}\b|\bxox[baprs]-[A-Za-z0-9-]{10,}|\bgh[pousr]_[A-Za-z0-9_]{20,}|\bsk-(?:proj-|ant-)?[A-Za-z0-9_-]{20,}|\bBearer\s+[A-Za-z0-9._-]+/i;

export function demoDenyPattern(customPattern) {
  return new RegExp(`(?:${DEFAULT_DENY})${customPattern ? `|(?:${customPattern})` : ""}`, "i");
}
const controlText = (locator, own = false) => locator.evaluate((el, own) => {
  // Own name: attributes, direct text, simple label children (a <span>Delete</span> inside a
  // trash zone), and label text without nested form controls. Nested item cards are skipped.
  const labelText = (l) => { const c = l.cloneNode(true); c.querySelectorAll("select, option, input, textarea, button").forEach((n) => n.remove()); return c.textContent; };
  const ownText = () => [...el.childNodes].filter((n) => n.nodeType === 3 || (n.nodeType === 1 && !n.children.length && n.getAttribute("draggable") !== "true" && !/^(option|optgroup)$/i.test(n.tagName))).map((n) => n.textContent).join(" ");
  const text = own ? ownText() : el.textContent;
  const label = (l) => (own ? labelText(l) : l.textContent);
  return [
    text, el.getAttribute("type"), el.getAttribute("name"), el.getAttribute("id"), el.getAttribute("autocomplete"),
    el.getAttribute("aria-label"), el.getAttribute("placeholder"), el.getAttribute("title"), el.getAttribute("value"),
    el.getAttribute("autocomplete") === "username" ? "credential" : "",
    ...(el.labels ? [...el.labels].map(label) : []),
    ...(el.getAttribute("aria-labelledby") || "").split(/\s+/).map((id) => el.ownerDocument.getElementById(id)?.textContent),
    el.closest("label") ? label(el.closest("label")) : "",
  ].filter(Boolean).join(" ");
}, own);

/**
 * action.type: "click" and "type" check all text; "drop" (drag ends) and "select" check the
 * control's own name. Credential checks apply to typing whatever the mode.
 */
export async function assertSafeDemoTarget(locator, action, deny) {
  const own = action.type === "drop" || action.type === "select";
  const actual = await controlText(locator, own);
  if (["click", "type", "drop", "select"].includes(action.type) && deny.test(actual)) throw new Error("refusing destructive-looking demo control");
  if (action.type === "type" && (SECRET_FIELD.test(`${action.selector || ""} ${actual}`) || SECRET_VALUE.test(String(action.text ?? "")))) throw new Error("refusing credential-looking demo field or value");
}
