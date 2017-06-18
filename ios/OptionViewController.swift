//
//  OptionViewController.swift
//  LetsTalk
//
//  Created by Arun Rawlani on 6/18/17.
//  Copyright © 2017 Arun Rawlani. All rights reserved.
//

import Foundation
import UIKit

class OptionViewController: UIViewController{
    @IBAction func unwindToOptionViewController (_ sender: UIStoryboardSegue){
        // bug? exit segue doesn't dismiss so we do it manually...
        self.dismiss(animated: true, completion: nil)
    }
}
