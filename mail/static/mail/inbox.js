document.addEventListener('DOMContentLoaded', function () {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  manage_form_fields('#compose-recipients');
  manage_form_fields('#compose-subject');
  manage_form_fields('#compose-body');
  // debugger// to pause and activate debug in chrome console 
  //send a mail to recipients when submit
  document.querySelector('#compose-form').onsubmit = function () {
    const recipients = manage_form_fields('#compose-recipients');
    const subject = manage_form_fields('#compose-subject');
    const body = manage_form_fields('#compose-body');
    //request to API
    fetch('/emails', {
        method: 'POST',
        body: JSON.stringify({
          recipients: recipients,
          subject: subject,
          body: body
        })
      })
      .then(status)
      .then(result => {
        // Print result
        console.log(result);
      });
    return false;
  };

}

function status(response) {
  if (response.ok) {
    if (response.status == 201) {
      load_mailbox('sent');
    }
    return response.json();
  } else {
    return Promise.reject(new Error(response.statusText))
  }
}

function manage_form_fields(formelement) {
  let value;
  value = document.querySelector(formelement).value;
  document.querySelector(formelement).value = '';
  return value
}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  
  //request to their respective mailbox
  // fetch('/emails/inbox')
  //   .then(response => response.json())
  //   .then(emails => {
  //     // Print emails
  //     console.log(emails);

  //     // ... do something else with emails ...
  //   });
}