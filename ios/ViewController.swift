//
//  ViewController.swift
//  LetsTalk
//
//  Created by Arun Rawlani on 6/16/17.
//  Copyright © 2017 Arun Rawlani. All rights reserved.
//

import UIKit

class ViewController: UIViewController {

    @IBAction func unwindToMainViewController (_ sender: UIStoryboardSegue){
        // bug? exit segue doesn't dismiss so we do it manually...
        self.dismiss(animated: true, completion: nil)
    }


}

