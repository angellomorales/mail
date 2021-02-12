let mailboxValue;
document.addEventListener('DOMContentLoaded', function () {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(contents) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-detail-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  if (contents.sender === undefined) {
    manage_form_fields('#compose-recipients');
    manage_form_fields('#compose-subject');
    manage_form_fields('#compose-body');
  } else {
    //prefill composition fields
    document.querySelector('#compose-recipients').value = contents.sender;
    if (contents.subject.startsWith('Re:')) {
      document.querySelector('#compose-subject').value = contents.subject;
    } else {
      document.querySelector('#compose-subject').value = `Re: ${contents.subject}`;
    }
    document.querySelector('#compose-body').value = `"On ${contents.timestamp} ${contents.sender} wrote:" ${contents.body}`;
  }
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
    //check status according to views.py and show sent page
    if (response.status == 201) {
      load_mailbox('sent');
      return response.json();
    }
    if (response.status == 204) {
      load_mailbox('inbox');
    }
  } else {
    return Promise.reject(new Error(response.statusText))
  }
}

function manage_form_fields(formelement) {
  //get value from fields and clean out
  let value;
  value = document.querySelector(formelement).value;
  document.querySelector(formelement).value = '';
  return value
}

function load_mailbox(mailbox) {
  mailboxValue = mailbox;
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-detail-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  //request to their respective mailbox
  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
      // Print emails
      console.log(`${mailbox}:`);
      console.log(emails);
      emails.forEach(add_mail);

      // ... do something else with emails ...
    });
}

function add_mail(contents) {
  //if the view is on sent page
  let title = contents.sender;
  if (mailboxValue == 'sent') {
    title = contents.recipients;
  }

  // create new body mail container 
  const bodyMailContainer = document.createElement('div');
  bodyMailContainer.className = 'body-mailContainer';
  bodyMailContainer.innerHTML = `<div><small>${contents.timestamp}</small></div><h5>${title}</h5><p>${contents.subject}</p>`;
  bodyMailContainer.addEventListener('click', () => {
    load_mail_detail(contents);
  });

  //Add archive button
  let archiveStatus = false;
  const archiveButton = document.createElement('button')
  archiveButton.className = 'btn btn-sm btn-outline-secondary';
  archiveButton.style.display = 'none';
  archiveButton.id = 'archive';
  if (mailboxValue == 'inbox') {
    archiveStatus = true;
    archiveButton.innerText = "archive";
  }
  if (mailboxValue == 'archive') {
    archiveStatus = false;
    archiveButton.innerText = "unarchive";
  }
  archiveButton.addEventListener('click', () => {
    archive_mail(contents, archiveStatus);
  });

  // create new footer mail container 
  const footerMailContainer = document.createElement('div');
  footerMailContainer.className = 'footer-mailContainer';
  footerMailContainer.append(archiveButton);

  //create mail container which contains body and footer
  const mailContainer = document.createElement('div');
  mailContainer.className = 'mailContainer';
  mailContainer.append(bodyMailContainer);
  mailContainer.append(footerMailContainer);

  if (contents.read) {
    mailContainer.style.backgroundColor = 'lightgrey';
    mailContainer.style.color = 'dimgray';
  }

  // Add mail container full to div emails-view 
  document.querySelector('#emails-view').append(mailContainer);

  //show archive buttons in mail container
  document.querySelectorAll('#archive').forEach(button => {
    if (mailboxValue == 'inbox' || mailboxValue == 'archive') {
      button.style.display = 'inline-block';
    } else {
      button.style.display = 'none';
    }
  });

};

function load_mail_detail(contents) {
  // Show the mail detail and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-detail-view').style.display = 'block';

  // Show the headers of the mail
  document.querySelector('#email-detail-view').innerHTML = `<div class="header"><strong>From: </strong>${contents.sender}<br>
  <strong>To: </strong>${contents.recipients}<br>
  <strong>Subject: </strong>${contents.subject}<br>
  <strong>Timestamp: </strong>${contents.timestamp}<br></div>`;

  //add reply button
  const replyButton = document.createElement('button');
  replyButton.className = 'btn btn-sm btn-outline-primary';
  replyButton.id = 'reply';
  replyButton.innerText = "Reply";
  replyButton.addEventListener('click', () => {
    reply_mail(contents);
  });

  //add hr separator
  const hr = document.createElement('hr');

  //add body mail
  const body = document.createElement('div');
  body.className = 'body-mail';
  body.innerHTML = `<p>${contents.body}</p>`

  //add elements to container
  document.querySelector('#email-detail-view').append(replyButton);
  document.querySelector('#email-detail-view').append(hr);
  document.querySelector('#email-detail-view').append(body);

  //request put to update read status

  fetch(`/emails/${contents.id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  });

}

function reply_mail(contents) {
  compose_email(contents);
}

function archive_mail(contents, archiveStatus) {
  //request put to update archived status when promise of fetch finish update inbox with .then status

  fetch(`/emails/${contents.id}`, {
      method: 'PUT',
      body: JSON.stringify({
        archived: archiveStatus
      })
    })
    .then(status);
}