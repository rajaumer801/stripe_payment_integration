Basic Stripe Payment Integration

1 - You can charge a user credit card using '/charge' endpoint.
2 - To add Stripe Connect Account (Merchant Account), you need to go through few steps:

	i - Send a link to new registered Merchant, link (Stripe authorization link) will 			include your Stripe Client Id and a unique string.
	ii - After filling the form provided on the link, Stripe will hit an url on your 			server with necessary information, you can use that information to transfer 			amount to Stripe Connect account.