document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector("#compose-form").onsubmit = send_email;

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Get emails to display from API request
  fetch(`/emails/${mailbox}`)
.then(response => response.json())
.then(emails =>{
    console.log(emails)
    emails.forEach(email => {
      // Create card for email
      const card = document.createElement("div");
      card.className = "card";
      if (email.read){
        card.style.backgroundColor = "rgb(230,230,230)";
      } else{
        card.style.backgroundColor = "white";
      }
      document.querySelector("#emails-view").append(card);

      // Create title of card
      const title = document.createElement("h4");
      title.className = "card-title";
      title.innerHTML = email.subject;
      card.append(title);
      
      // Create subtitle of card
      const subtitle = document.createElement("h6");
      subtitle.className = "card-subtitle";
      subtitle.innerHTML = email.sender;
      card.append(subtitle);

      // Create timestamp of card
      const timestamp = document.createElement("div");
      timestamp.className = "overflow";
      timestamp.innerHTML = email.timestamp;
      card.append(timestamp);

      // Create event listener for card
      card.addEventListener("click", function(){
        view_email(email,mailbox);
      });
    });
  });
}

function send_email() {

  // Get the entered values from the composed email
  const recipients = document.querySelector("#compose-recipients").value;
  const subject = document.querySelector("#compose-subject").value;
  const body = document.querySelector("#compose-body").value.replace(/\n/g,"<br />");

  // Send email through API call
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  })
  .then(response => response.json())
  .then(result => {
      // Check if there is an error
      if (result.error){
        alert(result.error);
        compose_email();
        // Prefill email form with previously entered information
        document.querySelector("#compose-recipients").value = recipients;
        document.querySelector("#compose-subject").value = subject;
        document.querySelector("#compose-body").value = body;
      } else{
        // If email was successful, return user to Sent Mailbox
        load_mailbox ('sent');
      }
  });

  return false;
}

function view_email(email,mailbox) {

  // Show the email and hide other views
  document.querySelector('#email-view').style.display = 'block';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Get the email div and reset
  div = document.querySelector("#email-view");
  div.innerHTML = "";

  // Create subject element
  const title = document.createElement("h3");
  div.append(title);
  title.innerHTML = `Subject: ${email.subject}`;

  // Create users element
  const users = document.createElement("div");
  div.append(users);
  users.className = "users";
  users.innerHTML = `FROM: ${email.sender}` + "<br />" + `TO: ${email.recipients}`;

  // Create body element
  const body = document.createElement("div");
  div.append(body);
  body.innerHTML = `${email.body} <hr />`;

  // Create timestamp element
  const timestamp = document.createElement("h6");
  div.append(timestamp);
  timestamp.innerHTML = email.timestamp;

  // Mark email as read
  fetch(`/emails/${email.id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })

  // Check if user is viewing Inbox mail
  if (mailbox === "inbox"){
    
    // Create reply button
    const reply_bttn = document.createElement('button');
    reply_bttn.className = "reply";
    div.append(reply_bttn);
    reply_bttn.innerHTML="Reply";
    reply_bttn.addEventListener('click', function() {
      compose_email();
      // Prefill email form
      document.querySelector("#compose-recipients").value = email.sender;
      if (!(email.subject.substring(0,4) === "Re: ")){
        document.querySelector("#compose-subject").value = `Re: ${email.subject}`;
      }
      document.querySelector("#compose-body").value = `On ${email.timestamp} ${email.sender} wrote: \n${email.body}\n`;
    });

    // Create archive button
    const archive_bttn = document.createElement('button');
    archive_bttn.className = "archive";
    div.append(archive_bttn);
    archive_bttn.innerHTML="Archive";
    archive_bttn.addEventListener('click', function() {
      // Mark email as archived
      fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
          archived: true
          })
      }).then(function(){
        load_mailbox('inbox');
      })
    });

  // Check if user is viewing Archive email  
  } else if (mailbox === "archive"){
    // Create unarchive button
    const archive_bttn = document.createElement('button');
    archive_bttn.className = "unarchive";
    div.append(archive_bttn);
    archive_bttn.innerHTML="Unarchive";
    archive_bttn.addEventListener('click', function() {
      // Mark email as not archived
      fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
          archived: false
          })
      }).then(function(){
        load_mailbox('inbox');
      })
    });
  }
}