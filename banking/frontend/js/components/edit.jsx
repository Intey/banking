import React from 'react'

/** Component for Edit something.
 * @param {String} Type of input, that represent edit value
 * @param {...} Value - initial of input
 * @param {String} FormName that for input will be attached
 * @param {Function} Change callback, on changing.
 * @param {Function} Focus callback, on focus.
 */
export default class Edit extends React.Component{
    render(){
        var errorHelper = !!this.props.error ?
            <span className="help-block">{this.props.erorr}</span> : null
        return (
            <div className={"input-group "+ (!!this.props.error ? "has-error" : "")}>
                <span className="input-group-addon">{this.props.Label}</span>
                <input type={this.props.Type} className="form-control"
                    value={this.props.Value} form={this.props.FormName}
                    onChange={this.props.Change} onFocus={this.props.Focus}/>
                {errorHelper}
            </div>
        );
    }
}
