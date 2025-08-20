function generateAlert(html, type, timeout = -1) {
  const alert = document.createElement('div');
  alert.classList.add('alert', `alert-${type}`, 'alert-dismissible', 'fade', 'show');
  alert.innerHTML = html + '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>'
  const bsAlert = new bootstrap.Alert(alert);
  if (timeout > 0) {
    setTimeout(() => {
      if (bsAlert) bsAlert.close();
    }, timeout);
  }
  return alert;
}
