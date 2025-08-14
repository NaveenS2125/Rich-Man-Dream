import * as React from "react"
import { ChevronDown, ChevronUp } from "lucide-react"
import { cn } from "../../lib/utils"

const Select = React.forwardRef(({ 
  children, 
  value, 
  onValueChange,
  disabled = false,
  ...props 
}, ref) => {
  const [isOpen, setIsOpen] = React.useState(false)
  const [selectedValue, setSelectedValue] = React.useState(value)

  React.useEffect(() => {
    setSelectedValue(value)
  }, [value])

  const handleValueChange = (newValue) => {
    setSelectedValue(newValue)
    if (onValueChange) {
      onValueChange(newValue)
    }
    setIsOpen(false)
  }

  return (
    <div className="relative" ref={ref} {...props}>
      {React.Children.map(children, child => {
        if (child.type === SelectTrigger) {
          return React.cloneElement(child, {
            isOpen,
            setIsOpen,
            selectedValue,
            disabled
          })
        }
        if (child.type === SelectContent) {
          return React.cloneElement(child, {
            isOpen,
            onValueChange: handleValueChange,
            selectedValue
          })
        }
        return child
      })}
    </div>
  )
})
Select.displayName = "Select"

const SelectTrigger = React.forwardRef(({ 
  className, 
  children, 
  isOpen, 
  setIsOpen, 
  disabled,
  ...props 
}, ref) => {
  return (
    <button
      className={cn(
        "flex h-10 w-full items-center justify-between rounded-md border border-gray-200 bg-white px-3 py-2 text-sm ring-offset-white placeholder:text-gray-500 focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 dark:border-gray-700 dark:bg-gray-800 dark:ring-offset-gray-900 dark:placeholder:text-gray-400 dark:focus:ring-yellow-400",
        className
      )}
      ref={ref}
      onClick={() => !disabled && setIsOpen(!isOpen)}
      disabled={disabled}
      {...props}
    >
      <span>{children}</span>
      {isOpen ? (
        <ChevronUp className="h-4 w-4 opacity-50" />
      ) : (
        <ChevronDown className="h-4 w-4 opacity-50" />
      )}
    </button>
  )
})
SelectTrigger.displayName = "SelectTrigger"

const SelectValue = ({ placeholder, selectedValue }) => {
  return (
    <span className={cn(
      selectedValue ? "text-gray-900 dark:text-white" : "text-gray-500 dark:text-gray-400"
    )}>
      {selectedValue || placeholder}
    </span>
  )
}
SelectValue.displayName = "SelectValue"

const SelectContent = React.forwardRef(({ 
  className, 
  children, 
  isOpen, 
  onValueChange, 
  selectedValue,
  ...props 
}, ref) => {
  if (!isOpen) return null

  return (
    <div
      className={cn(
        "absolute top-full z-50 mt-1 max-h-60 w-full overflow-auto rounded-md border border-gray-200 bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none dark:border-gray-700 dark:bg-gray-800",
        className
      )}
      ref={ref}
      {...props}
    >
      {React.Children.map(children, child => {
        if (child.type === SelectItem) {
          return React.cloneElement(child, {
            onValueChange,
            selectedValue,
            isSelected: child.props.value === selectedValue
          })
        }
        return child
      })}
    </div>
  )
})
SelectContent.displayName = "SelectContent"

const SelectItem = React.forwardRef(({ 
  className, 
  children, 
  value, 
  onValueChange, 
  isSelected,
  ...props 
}, ref) => {
  return (
    <div
      className={cn(
        "relative cursor-pointer select-none py-2 px-3 text-sm hover:bg-gray-100 dark:hover:bg-gray-700",
        isSelected && "bg-yellow-50 text-yellow-900 dark:bg-yellow-900/30 dark:text-yellow-400",
        className
      )}
      ref={ref}
      onClick={() => onValueChange(value)}
      {...props}
    >
      {children}
      {isSelected && (
        <span className="absolute inset-y-0 right-0 flex items-center pr-4">
          <svg className="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
          </svg>
        </span>
      )}
    </div>
  )
})
SelectItem.displayName = "SelectItem"

export {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
}