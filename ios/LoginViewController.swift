//
//  LoginViewController.swift
//  LetsTalk
//
//  Created by Arun Rawlani on 6/16/17.
//  Copyright © 2017 Arun Rawlani. All rights reserved.
//

import Foundation
import UIKit

class LoginViewController: UIViewController{
    //@IBOutlet weak var aIndicator: UIActivityIndicatorView!
    @IBOutlet weak var aIndi: UIActivityIndicatorView!
    
    override func viewDidLoad() {
        self.aIndi.isHidden = true;
        self.aIndi.hidesWhenStopped = true
    }
    
    @IBAction func loginPressed(_ sender: Any) {
        let when = DispatchTime.now() + 2
        self.aIndi.isHidden = false;
        
        //method to produce delay and show Activity Indicator
        self.aIndi.startAnimating()
        DispatchQueue.main.asyncAfter(deadline: when){
            self.aIndi.stopAnimating()
        }
        self.performSegue(withIdentifier: "welcomeSegue", sender: self)
    }
    
}
